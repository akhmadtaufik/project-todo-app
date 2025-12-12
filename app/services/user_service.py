"""
User Service

Business logic for user operations.
"""
from typing import List, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.core.extensions import db
from app.core.security import hash_password
from app.models.user import Users
from app.schemas.user import UserResponse, UserBasicResponse, UserWithProjects


class UserService:
    """Service class for user operations."""

    @staticmethod
    def get_all_users(page: int = 1, per_page: int = 10) -> dict:
        """
        Get all users with pagination.
        
        Uses joinedload to eager load projects and prevent N+1 queries.
        
        Args:
            page: Page number (1-indexed)
            per_page: Number of items per page
        
        Returns:
            Dictionary with 'data' and 'meta' keys for paginated response
        """
        # Use joinedload to fetch users and their projects in a single query
        pagination = Users.query.options(
            joinedload(Users.projects)
        ).paginate(page=page, per_page=per_page, error_out=False)
        data = [
            {
                "user_id": user.id,
                "name": user.name,
                "email": user.email,
                "created_at": str(user.created_at) if user.created_at else None,
                "update_at": str(user.update_at) if user.update_at else None
            }
            for user in pagination.items
        ]
        return {
            "data": data,
            "meta": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_pages": pagination.pages,
                "total_items": pagination.total
            }
        }

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Users]:
        """Get a user by ID."""
        return Users.query.get(user_id)

    @staticmethod
    def check_user_permission(current_user_id: str, target_user_id: int) -> bool:
        """Check if current user has permission to access target user's data."""
        return str(current_user_id) == str(target_user_id)

    @staticmethod
    def update_user(user: Users, name: str, email: str, password: str) -> Users:
        """
        Update user information.
        
        Args:
            user: User model instance
            name: New name
            email: New email
            password: New password (will be hashed)
            
        Returns:
            Updated user model
        """
        user.name = name
        user.email = email
        user.password = hash_password(password)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user: Users) -> Tuple[bool, str]:
        """
        Delete a user.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            db.session.delete(user)
            db.session.commit()
            return True, "User successfully deleted"
        except SQLAlchemyError:
            db.session.rollback()
            return False, "Error deleting user"

    @staticmethod
    def serialize_user(user: Users) -> dict:
        """Serialize user to dictionary format."""
        return UserResponse.from_orm_user(user).model_dump()

    @staticmethod
    def serialize_user_basic(user: Users) -> dict:
        """Serialize user with basic fields only."""
        return UserBasicResponse.from_orm_user(user).model_dump()

    @staticmethod
    def serialize_user_with_projects(user: Users) -> dict:
        """Serialize user with projects included."""
        return UserWithProjects.from_orm_user(user).model_dump()
