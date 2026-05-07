from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ColumnBase(BaseModel):
    name: str
    order: float = 0.0


class ColumnCreate(ColumnBase):
    pass


class ColumnUpdate(BaseModel):
    name: str | None = None
    order: float | None = None


class ColumnResponse(ColumnBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime | None = None


class ColumnWithTasks(ColumnResponse):
    tasks: list = []
