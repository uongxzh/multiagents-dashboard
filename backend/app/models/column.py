import uuid

from sqlalchemy import Column, String, DateTime, Float, func

from app.db.database import Base


class Column_(Base):
    __tablename__ = "columns"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    order = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
