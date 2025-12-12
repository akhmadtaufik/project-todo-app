"""
Security Utilities

Password hashing, verification, and JWT token revocation.
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from app.core.extensions import db, jwt


def hash_password(password: str) -> str:
    """Hash a password using werkzeug's secure hashing (bcrypt-like)."""
    return generate_password_hash(password, method='pbkdf2:sha256:600000')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return check_password_hash(password_hash, password)


# JWT Token Revocation Callback
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    """
    Callback to check if a JWT token has been revoked.
    Called automatically by Flask-JWT-Extended on every protected route.
    """
    from app.models.token_blocklist import TokenBlocklist
    jti = jwt_payload["jti"]
    return TokenBlocklist.is_token_revoked(jti)


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """Callback when a revoked token is used."""
    return {
        "success": False,
        "error": {
            "code": 401,
            "message": "Token has been revoked"
        }
    }, 401


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Callback when an expired token is used."""
    return {
        "success": False,
        "error": {
            "code": 401,
            "message": "Token has expired"
        }
    }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Callback when an invalid token is used."""
    return {
        "success": False,
        "error": {
            "code": 401,
            "message": "Invalid token"
        }
    }, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Callback when no token is provided."""
    return {
        "success": False,
        "error": {
            "code": 401,
            "message": "Authorization token required"
        }
    }, 401
