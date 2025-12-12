"""
Task Schemas

Pydantic models for Task request/response validation.
"""
from datetime import datetime, date
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, field_validator


class TaskBase(BaseModel):
    """Base task schema with common fields."""
    task_name: str
    description: Optional[str] = None
    due_date: str  # Accept as string, validate format
    status: Optional[str] = None


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    project_id: int

    @field_validator('due_date')
    @classmethod
    def validate_due_date(cls, v):
        """Validate due date format and ensure it's not in the past."""
        try:
            due = datetime.strptime(v, "%Y-%m-%d").date()
            if due < date.today():
                raise ValueError("Due date must be later than the current date")
            return v
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
            raise


class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    task_name: str
    description: Optional[str] = None
    due_date: str
    status: Optional[str] = None


class TaskResponse(BaseModel):
    """Schema for task response."""
    model_config = ConfigDict(from_attributes=True)
    
    task_id: int
    task_name: str
    description: Optional[str] = None
    due_date: Optional[Any] = None
    status: Optional[str] = None
    project_id: int
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None

    @classmethod
    def from_orm_task(cls, task) -> "TaskResponse":
        """Create TaskResponse from SQLAlchemy Task model."""
        return cls(
            task_id=task.id,
            task_name=task.task_name,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            project_id=task.project_id,
            created_at=task.created_at,
            update_at=task.update_at
        )


class TaskBasicResponse(BaseModel):
    """Basic task response for updates."""
    model_config = ConfigDict(from_attributes=True)
    
    task_name: str
    description: Optional[str] = None
    due_date: Optional[Any] = None
    status: Optional[str] = None
    update_at: Optional[datetime] = None

    @classmethod
    def from_orm_task(cls, task) -> "TaskBasicResponse":
        """Create TaskBasicResponse from SQLAlchemy Task model."""
        return cls(
            task_name=task.task_name,
            description=task.description,
            due_date=task.due_date,
            status=task.status,
            update_at=task.update_at
        )
