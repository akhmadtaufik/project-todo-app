"""
Authentication API Routes

Handles user registration, login, token refresh, and logout.
Strict rate limiting applied for security.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from pydantic import ValidationError

from app.api import auth_bp
from app.core.extensions import limiter
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService


def parse_request_body(schema_class):
    """Parse and validate request body with Pydantic schema."""
    data = request.get_json()
    if not data:
        return None, {"success": False, "error": {"code": 400, "message": "No data provided"}}
    try:
        return schema_class(**data), None
    except ValidationError as e:
        # Return sanitized field errors (no internal details)
        errors = []
        for err in e.errors():
            field = ".".join(str(loc) for loc in err["loc"])
            msg = err["msg"]
            # Sanitize message - remove internal details
            if "string" in msg.lower():
                msg = f"Invalid {field} format"
            errors.append({"field": field, "message": msg})
        return None, {"success": False, "error": {"code": 422, "message": "Validation error", "details": errors}}


@auth_bp.route("/register", methods=["POST"], strict_slashes=False)
@limiter.limit("5 per minute")  # Strict limit for registration
def registration():
    """
    Register a new user.
    
    Returns:
        201: Registration successful
        422: Validation error
    """
    validated, error = parse_request_body(RegisterRequest)
    if error:
        return jsonify(error), error["error"]["code"]
    
    success, message, user = AuthService.register_user(
        validated.name,
        validated.email,
        validated.password
    )
    
    if success:
        return jsonify({"success": True, "message": message}), 201
    else:
        return jsonify({"success": False, "error": {"code": 422, "message": message}}), 422


@auth_bp.route("/login", methods=["POST"], strict_slashes=False)
@limiter.limit("5 per minute")  # Strict limit for login (prevents brute force)
def login():
    """
    Login with user credentials.
    
    Returns:
        200: Login successful with tokens
        400: Incomplete data
        401: Invalid credentials
    """
    validated, error = parse_request_body(LoginRequest)
    if error:
        return jsonify(error), error["error"]["code"]
    
    success, message, user = AuthService.authenticate_user(
        validated.email,
        validated.password
    )
    
    if not success:
        # Generic error message for security (don't reveal if email exists)
        return jsonify({
            "success": False,
            "error": {"code": 401, "message": "Invalid email or password"}
        }), 401
    
    access_token, refresh_token = AuthService.create_tokens(user.id)
    
    return jsonify({
        "success": True,
        "message": message,
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


@auth_bp.route("/refresh", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
@limiter.limit("30 per hour")
def refresh():
    """
    Refresh the access token.
    
    Returns:
        200: New access token
    """
    current_user = get_jwt_identity()
    new_token = AuthService.refresh_access_token(current_user)
    
    return jsonify({
        "success": True,
        "access_token": new_token
    }), 200


@auth_bp.route("/logout", methods=["POST"], strict_slashes=False)
@jwt_required()
def logout():
    """
    Logout the current user by revoking their token.
    
    Returns:
        200: Successfully logged out
    """
    jwt = get_jwt()
    jti = jwt["jti"]
    token_type = jwt["type"]
    current_user = get_jwt_identity()
    
    success, message = AuthService.logout(jti, token_type, current_user)
    
    if success:
        return jsonify({"success": True, "message": message}), 200
    else:
        return jsonify({"success": False, "error": {"code": 500, "message": "Logout failed"}}), 500
