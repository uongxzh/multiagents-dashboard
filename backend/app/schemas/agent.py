from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AgentBase(BaseModel):
    name: str
    role: str
    description: str | None = None
    runtime_id: str | None = None
    environment: str = "unknown"
    status: str = "idle"
    avatar: str | None = None


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    description: str | None = None
    runtime_id: str | None = None
    environment: str | None = None
    status: str | None = None
    avatar: str | None = None


class AgentResponse(AgentBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime | None = None
