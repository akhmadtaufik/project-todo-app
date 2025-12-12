"""
Project Schemas

Pydantic models for Project request/response validation.
"""
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    """Base project schema with common fields."""
    project_name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""
    pass


class ProjectUpdate(ProjectBase):
    """Schema for updating a project."""
    pass


class TaskInProject(BaseModel):
    """Nested task schema for project responses."""
    model_config = ConfigDict(from_attributes=True)
    
    task_id: int
    task_name: str
    description: Optional[str] = None
    due_date: Optional[Any] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class ProjectResponse(BaseModel):
    """Schema for project response."""
    model_config = ConfigDict(from_attributes=True)
    
    project_id: int
    project_name: str
    description: Optional[str] = None
    user_id: int
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None

    @classmethod
    def from_orm_project(cls, project) -> "ProjectResponse":
        """Create ProjectResponse from SQLAlchemy Project model."""
        return cls(
            project_id=project.id,
            project_name=project.project_name,
            description=project.description,
            user_id=project.user_id,
            created_at=project.created_at,
            update_at=project.update_at
        )


class ProjectBasicResponse(BaseModel):
    """Basic project response for updates."""
    model_config = ConfigDict(from_attributes=True)
    
    project_name: str
    description: Optional[str] = None
    update_at: Optional[datetime] = None

    @classmethod
    def from_orm_project(cls, project) -> "ProjectBasicResponse":
        """Create ProjectBasicResponse from SQLAlchemy Project model."""
        return cls(
            project_name=project.project_name,
            description=project.description,
            update_at=project.update_at
        )


class ProjectWithTasks(ProjectResponse):
    """Project response including tasks list."""
    task: List[Any] = []

    @classmethod
    def from_orm_project(cls, project) -> "ProjectWithTasks":
        """Create ProjectWithTasks from SQLAlchemy Project model."""
        from app.schemas.task import TaskResponse
        return cls(
            project_id=project.id,
            project_name=project.project_name,
            description=project.description,
            user_id=project.user_id,
            created_at=project.created_at,
            update_at=project.update_at,
            task=[TaskResponse.from_orm_task(t) for t in project.tasks]
        )
