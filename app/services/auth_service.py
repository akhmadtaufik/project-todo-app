"""
Authentication Service

Business logic for user authentication and registration.
"""
from typing import Optional, Tuple
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError

from app.core.extensions import db
from app.core.security import hash_password, verify_password
from app.models.user import Users


class AuthService:
    """Service class for authentication operations."""

    @staticmethod
    def register_user(name: str, email: str, password: str) -> Tuple[bool, str, Optional[Users]]:
        """
        Register a new user.
        
        Returns:
            Tuple of (success, message, user)
        """
        if not name or not email or not password:
            return False, "Incomplete data. Please provide all required fields.", None

        hashed_password = hash_password(password)
        
        try:
            user = Users(name=name, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return True, "Registration user is completed", user
        except IntegrityError:
            db.session.rollback()
            return False, f"Email '{email}' is already registered.", None

    @staticmethod
    def authenticate_user(email: str, password: str) -> Tuple[bool, str, Optional[Users]]:
        """
        Authenticate a user with email and password.
        
        Returns:
            Tuple of (success, message, user)
        """
        if not email or not password:
            return False, "Incomplete data. Please provide all required fields.", None

        user = Users.query.filter_by(email=email).first()
        
        if not user:
            return False, "User not found", None

        if not verify_password(password, user.password):
            return False, "Invalid credentials. Check your password.", None

        return True, "Login successfully", user

    @staticmethod
    def create_tokens(user_id: int) -> Tuple[str, str]:
        """
        Create access and refresh tokens for a user.
        
        Returns:
            Tuple of (access_token, refresh_token)
        """
        access_token = create_access_token(identity=str(user_id))
        refresh_token = create_refresh_token(identity=str(user_id))
        return access_token, refresh_token

    @staticmethod
    def refresh_access_token(user_id: str) -> str:
        """Create a new access token from a refresh token."""
        return create_access_token(identity=user_id)
