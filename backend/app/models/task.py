import uuid

from sqlalchemy import Column, String, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    description = Column(String, nullable=True)
    status = Column(String(20), nullable=False, default="todo")
    priority = Column(String(10), nullable=False, default="medium")
    assignee_agent_id = Column(String, ForeignKey("agents.id", ondelete="SET NULL"), nullable=True)
    creator_id = Column(String, nullable=True)
    column_position = Column(Float, nullable=False, default=0.0)
    column_id = Column(String, ForeignKey("columns.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    due_date = Column(DateTime, nullable=True)

    assignee = relationship("Agent", foreign_keys=[assignee_agent_id], lazy="joined")
    column_rel = relationship("Column_", foreign_keys=[column_id], lazy="joined")
