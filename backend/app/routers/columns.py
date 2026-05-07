from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.column import Column_
from app.models.task import Task
from app.schemas.column import ColumnCreate, ColumnResponse, ColumnUpdate
from app.schemas.common import err, ok
from app.schemas.task import TaskResponse

router = APIRouter(tags=["columns"])


@router.get("/api/columns")
def list_columns(db: Session = Depends(get_db)):
    columns = db.query(Column_).order_by(Column_.order).all()
    result = []
    for col in columns:
        tasks = (
            db.query(Task)
            .filter(Task.column_id == col.id)
            .order_by(Task.column_position)
            .all()
        )
        result.append(
            {
                "id": col.id,
                "name": col.name,
                "order": col.order,
                "created_at": col.created_at,
                "tasks": [TaskResponse.model_validate(t) for t in tasks],
            }
        )
    return ok(result)


@router.post("/api/columns", status_code=201)
def create_column(data: ColumnCreate, db: Session = Depends(get_db)):
    col = Column_(**data.model_dump())
    db.add(col)
    db.commit()
    db.refresh(col)
    return ok(ColumnResponse.model_validate(col))


@router.put("/api/columns/{column_id}")
def update_column(column_id: str, data: ColumnUpdate, db: Session = Depends(get_db)):
    col = db.query(Column_).filter(Column_.id == column_id).first()
    if not col:
        return err("NOT_FOUND", "Column not found", 404)
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(col, key, val)
    db.commit()
    db.refresh(col)
    return ok(ColumnResponse.model_validate(col))


@router.delete("/api/columns/{column_id}", status_code=204)
def delete_column(column_id: str, db: Session = Depends(get_db)):
    col = db.query(Column_).filter(Column_.id == column_id).first()
    if not col:
        return err("NOT_FOUND", "Column not found", 404)
    db.delete(col)
    db.commit()
