from uuid import uuid4
from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Enum as SAEnum, JSON, Text, func
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects import postgresql
from app.common.enums import TaskKind, MediaKind, TaskStatus
from sqlalchemy.dialects.postgresql import UUID

    
# --- 提交记录表 ---
class Submission(Base):
    __tablename__ = "submissions"
    
    id: Mapped[int] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # To-do: default = 1, ForeignKey
    user_id: Mapped[int] = mapped_column(Integer, default=1)
    task: Mapped[TaskKind] = mapped_column(SAEnum(TaskKind))
    media: Mapped[MediaKind] = mapped_column(SAEnum(MediaKind))
    # To-do: Minio Key
    storage_key: Mapped[str] = mapped_column(String(512))
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus), 
        default=TaskStatus.pending, 
        server_default=TaskStatus.pending.value, 
        index=True
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )
    result: Mapped[Optional[dict]] = mapped_column(
        JSON().with_variant(postgresql.JSONB, "postgresql"),
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        default=None,
        onupdate=func.now(),
        server_onupdate=func.now(),
        nullable=True
    )
    
    