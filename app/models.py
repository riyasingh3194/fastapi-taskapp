import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base
import uuid

class Task(Base):
    __tablename__ = "tasks"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = sa.Column(sa.String(256), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    status = sa.Column(sa.Enum("pending", "in-progress", "completed", name="task_status"), nullable=False, server_default="pending")
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
