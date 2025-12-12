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
    Register a new user
    ---
    tags:
      - Authentication
    security: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - email
              - password
            properties:
              name:
                type: string
                minLength: 2
                maxLength: 100
                example: John Doe
              email:
                type: string
                format: email
                example: john@example.com
              password:
                type: string
                minLength: 8
                maxLength: 128
                description: Must contain at least one letter and one number
                example: SecurePass123
    responses:
      201:
        description: Registration successful
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: User registered successfully
      422:
        description: Validation error or email already exists
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: false
                error:
                  type: object
                  properties:
                    code:
                      type: integer
                      example: 422
                    message:
                      type: string
                      example: Email already registered
      429:
        description: Rate limit exceeded
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
    Login with user credentials
    ---
    tags:
      - Authentication
    security: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - email
              - password
            properties:
              email:
                type: string
                format: email
                example: john@example.com
              password:
                type: string
                example: SecurePass123
    responses:
      200:
        description: Login successful with JWT tokens
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: Login successful
                access_token:
                  type: string
                  description: JWT access token (expires in 1 hour)
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                refresh_token:
                  type: string
                  description: JWT refresh token (expires in 30 days)
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      401:
        description: Invalid credentials
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: false
                error:
                  type: object
                  properties:
                    code:
                      type: integer
                      example: 401
                    message:
                      type: string
                      example: Invalid email or password
      429:
        description: Rate limit exceeded
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
    Refresh the access token
    ---
    tags:
      - Authentication
    security:
      - BearerAuth: []
    description: Use the refresh token in the Authorization header to get a new access token
    responses:
      200:
        description: New access token generated
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                access_token:
                  type: string
                  description: New JWT access token
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      401:
        description: Invalid or expired refresh token
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: Token has expired
      429:
        description: Rate limit exceeded
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
    Logout the current user
    ---
    tags:
      - Authentication
    security:
      - BearerAuth: []
    description: Revokes the current JWT token, preventing further use
    responses:
      200:
        description: Successfully logged out
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                message:
                  type: string
                  example: Successfully logged out
      401:
        description: Missing or invalid token
        content:
          application/json:
            schema:
              type: object
              properties:
                msg:
                  type: string
                  example: Missing Authorization Header
      500:
        description: Logout failed
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

