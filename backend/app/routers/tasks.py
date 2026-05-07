from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.task import Task
from app.schemas.common import err, ok
from app.schemas.task import TaskCreate, TaskMove, TaskResponse, TaskUpdate

router = APIRouter(tags=["tasks"])


@router.get("/api/tasks")
def list_tasks(
    status: str | None = Query(None),
    priority: str | None = Query(None),
    assignee: str | None = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if assignee:
        query = query.filter(Task.assignee_agent_id == assignee)
    tasks = query.order_by(Task.column_position).all()
    return ok([TaskResponse.model_validate(t) for t in tasks])


@router.post("/api/tasks", status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    task = Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return ok(TaskResponse.model_validate(task))


@router.get("/api/tasks/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return err("NOT_FOUND", "Task not found", 404)
    return ok(TaskResponse.model_validate(task))


@router.put("/api/tasks/{task_id}")
def update_task(task_id: str, data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return err("NOT_FOUND", "Task not found", 404)
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(task, key, val)
    db.commit()
    db.refresh(task)
    return ok(TaskResponse.model_validate(task))


@router.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return err("NOT_FOUND", "Task not found", 404)
    db.delete(task)
    db.commit()


@router.patch("/api/tasks/{task_id}/move")
def move_task(task_id: str, data: TaskMove, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return err("NOT_FOUND", "Task not found", 404)
    task.column_id = data.column_id
    if data.column_position is not None:
        task.column_position = data.column_position
    db.commit()
    db.refresh(task)
    return ok(TaskResponse.model_validate(task))
