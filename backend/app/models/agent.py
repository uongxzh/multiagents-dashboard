import uuid

from sqlalchemy import Column, String, DateTime, func

from app.db.database import Base


class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False, unique=True)
    role = Column(String(50), nullable=False)
    description = Column(String, nullable=True)
    runtime_id = Column(String(100), nullable=True)
    environment = Column(String(50), nullable=False, default="unknown")
    status = Column(String(20), nullable=False, default="idle")
    avatar = Column(String(10), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
