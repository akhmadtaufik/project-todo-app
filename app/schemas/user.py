"""
User Schemas

Pydantic models for User request/response validation.
"""
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base user schema with common fields."""
    name: str
    email: str


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response without sensitive data."""
    model_config = ConfigDict(from_attributes=True)
    
    user_id: int
    name: str
    email: str
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None

    @classmethod
    def from_orm_user(cls, user) -> "UserResponse":
        """Create UserResponse from SQLAlchemy User model."""
        return cls(
            user_id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            update_at=user.update_at
        )


class UserBasicResponse(BaseModel):
    """Basic user response for updates."""
    model_config = ConfigDict(from_attributes=True)
    
    username: str
    email: str
    update_at: Optional[datetime] = None

    @classmethod
    def from_orm_user(cls, user) -> "UserBasicResponse":
        """Create UserBasicResponse from SQLAlchemy User model."""
        return cls(
            username=user.name,
            email=user.email,
            update_at=user.update_at
        )


class ProjectInUser(BaseModel):
    """Nested project schema for user responses."""
    model_config = ConfigDict(from_attributes=True)
    
    project_id: int
    project_name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    update_at: Optional[datetime] = None


class UserWithProjects(UserResponse):
    """User response including projects list."""
    project_list: List[Any] = []

    @classmethod
    def from_orm_user(cls, user) -> "UserWithProjects":
        """Create UserWithProjects from SQLAlchemy User model."""
        from app.schemas.project import ProjectWithTasks
        return cls(
            user_id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            update_at=user.update_at,
            project_list=[ProjectWithTasks.from_orm_project(p) for p in user.projects]
        )
