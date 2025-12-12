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
def check_if_token_revoked(jwt_header, jwt_payload) -> bool:
    """
    Callback to check if a JWT token has been revoked.
    Called automatically by Flask-JWT-Extended on every protected route.
    
    Checks two revocation methods:
    1. TokenBlocklist: individual token revocation (logout)
    2. token_valid_after: timestamp-based bulk revocation (force logout all devices)
    
    Returns:
        True if token is revoked, False otherwise
    """
    from app.models.token_blocklist import TokenBlocklist
    from app.models.user import Users
    
    jti = jwt_payload["jti"]
    
    # Check 1: Is token in blocklist? (individual revocation)
    if TokenBlocklist.is_token_revoked(jti):
        return True
    
    # Check 2: Timestamp-based revocation
    # Get user ID and token issued-at time
    user_id = jwt_payload.get("sub")  # User ID stored as 'sub' claim
    iat = jwt_payload.get("iat")  # Issued At timestamp
    
    if user_id and iat:
        try:
            user = Users.query.get(int(user_id))
            if user and user.token_valid_after:
                # Convert iat to datetime for comparison
                token_issued_at = datetime.fromtimestamp(iat)
                # If token was issued before token_valid_after, it's revoked
                if token_issued_at < user.token_valid_after:
                    return True
        except (ValueError, TypeError):
            # If we can't parse the user_id, default to not revoked
            pass
    
    return False


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
