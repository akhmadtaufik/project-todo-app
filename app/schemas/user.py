"""
User Schemas

Pydantic models with strict validation for User operations.
"""
import re
import bleach
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


def sanitize_string(value: str, max_length: int = 255) -> str:
    """Sanitize string input - strip, limit length, remove HTML."""
    if not value:
        return value
    value = value.strip()
    value = bleach.clean(value, tags=[], strip=True)
    return value[:max_length]


class UserBase(BaseModel):
    """Base user schema with common validated fields."""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Sanitize name field."""
        return sanitize_string(v, 100)


class UserCreate(UserBase):
    """Schema for creating a new user with password validation."""
    password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r'[A-Za-z]', v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one number")
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user with validation."""
    username: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Sanitize username field."""
        return sanitize_string(v, 100)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


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
