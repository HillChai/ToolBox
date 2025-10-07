from __future__ import annotations
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.common.enums import TaskKind, MediaKind, TaskStatus

    
class ORMBase(BaseModel):
    """开启 Pydantic v2 ORM 模式"""
    model_config = ConfigDict(from_attributes=True)
    

class SubmissionCreate(BaseModel):
    """创建任务"""
    user_id: int = Field(default=1, ge=1)
    task: TaskKind
    media: MediaKind
    storage_key: str


class SubmissionStatusUpdate(BaseModel):
    """执行阶段更新"""
    status: TaskStatus
    error_message: Optional[str] = None 
    result: Optional[Dict[str, Any]] = None
    
    
class SubmissionRead(ORMBase):
    """查询任务执行状态"""
    id: str
    user_id: int
    task: TaskKind
    media: MediaKind
    storage_key: str
    status: TaskStatus
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

    created_at: datetime
    updated_at: Optional[datetime] = None
    
    
    