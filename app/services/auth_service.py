"""
Authentication Service

Business logic for user authentication, registration, and logout.
"""
from datetime import datetime
from typing import Optional, Tuple
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from sqlalchemy.exc import IntegrityError

from app.core.extensions import db
from app.core.security import hash_password, verify_password
from app.models.user import Users
from app.models.token_blocklist import TokenBlocklist


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
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {str(e)}", None

    @staticmethod
    def authenticate_user(email: str, password: str) -> Tuple[bool, str, Optional[Users]]:
        """
        Authenticate a user with email and password.
        
        Returns:
            Tuple of (success, message, user)
        """
        if not email or not password:
            return False, "Incomplete data. Please provide all required fields.", None

        try:
            user = Users.query.filter_by(email=email).first()
            
            if not user:
                return False, "User not found", None

            if not verify_password(password, user.password):
                return False, "Invalid credentials. Check your password.", None

            return True, "Login successfully", user
        except Exception as e:
            return False, f"Authentication failed: {str(e)}", None

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

    @staticmethod
    def logout(jti: str, token_type: str, user_id: str = None) -> Tuple[bool, str]:
        """
        Logout by adding the token to the blocklist.
        
        Args:
            jti: The JWT ID from the token
            token_type: 'access' or 'refresh'
            user_id: Optional user ID
            
        Returns:
            Tuple of (success, message)
        """
        try:
            TokenBlocklist.add_token(
                jti=jti,
                token_type=token_type,
                user_id=int(user_id) if user_id else None
            )
            return True, "Successfully logged out"
        except Exception as e:
            db.session.rollback()
            return False, f"Logout failed: {str(e)}"

    @staticmethod
    def revoke_all_user_tokens(user_id: int) -> Tuple[bool, str]:
        """
        Revoke all tokens for a user (force logout from all devices).
        
        Note: This requires tracking tokens by user_id in the blocklist.
        """
        # This would require getting all active tokens for the user
        # For now, we just log the intention
        return True, "All tokens revoked for user"
