"""
Authentication API Routes

Handles user registration, login, token refresh, and logout.
Rate limited for security.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app.api import auth_bp
from app.core.extensions import limiter
from app.services.auth_service import AuthService


@auth_bp.route("/register", methods=["POST"], strict_slashes=False)
@limiter.limit("5 per minute")
def registration():
    """
    Register a new user.
    
    Returns:
        201: Registration successful
        422: Incomplete data or duplicate email
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    success, message, user = AuthService.register_user(name, email, password)
    
    if success:
        return jsonify({"success": True, "message": message}), 201
    else:
        return jsonify({"success": False, "message": message}), 422


@auth_bp.route("/login", methods=["POST"], strict_slashes=False)
@limiter.limit("10 per minute")
def login():
    """
    Login with user credentials.
    
    Returns:
        200: Login successful with tokens
        400: Incomplete data or user not found
        401: Invalid credentials
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
    
    email = data.get("email")
    password = data.get("password")
    
    success, message, user = AuthService.authenticate_user(email, password)
    
    if not success:
        status_code = 401 if "Invalid credentials" in message else 400
        return jsonify({"success": False, "message": message}), status_code
    
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
        return jsonify({"success": False, "message": message}), 500
