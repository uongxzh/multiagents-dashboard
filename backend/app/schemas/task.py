from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.agent import AgentResponse


class TaskBase(BaseModel):
    title: str
    description: str | None = None
    status: str = "todo"
    priority: str = "medium"
    assignee_agent_id: str | None = None
    column_id: str | None = None
    column_position: float = 0.0
    due_date: datetime | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"todo", "in_progress", "in_review", "done"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str) -> str:
        allowed = {"low", "medium", "high", "urgent"}
        if v not in allowed:
            raise ValueError(f"priority must be one of {allowed}")
        return v


class TaskCreate(TaskBase):
    creator_id: str | None = None
    pass


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    assignee_agent_id: str | None = None
    column_id: str | None = None
    column_position: float | None = None
    due_date: datetime | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        if v is None:
            return v
        allowed = {"todo", "in_progress", "in_review", "done"}
        if v not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, v: str | None) -> str | None:
        if v is None:
            return v
        allowed = {"low", "medium", "high", "urgent"}
        if v not in allowed:
            raise ValueError(f"priority must be one of {allowed}")
        return v


class TaskMove(BaseModel):
    column_id: str
    column_position: float | None = None


class TaskResponse(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    creator_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    assignee: AgentResponse | None = None
