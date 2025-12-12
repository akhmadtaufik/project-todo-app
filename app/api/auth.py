"""
Authentication API Routes

Handles user registration, login, and token refresh.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api import auth_bp
from app.services.auth_service import AuthService


@auth_bp.route("/register", methods=["POST"], strict_slashes=False)
def registration():
    """
    Register a new user.
    
    Returns:
        201: Registration successful
        422: Incomplete data or duplicate email
    """
    data = request.get_json()
    
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    
    success, message, user = AuthService.register_user(name, email, password)
    
    if success:
        return jsonify({"message": message}), 201
    else:
        return jsonify({"message": message}), 422


@auth_bp.route("/login", methods=["POST"], strict_slashes=False)
def login():
    """
    Login with user credentials.
    
    Returns:
        200: Login successful with tokens
        400: Incomplete data or user not found
        401: Invalid credentials
    """
    data = request.get_json()
    
    email = data.get("email")
    password = data.get("password")
    
    success, message, user = AuthService.authenticate_user(email, password)
    
    if not success:
        status_code = 401 if "Invalid credentials" in message else 400
        return jsonify({"message": message}), status_code
    
    access_token, refresh_token = AuthService.create_tokens(user.id)
    
    return jsonify({
        "message": message,
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 200


@auth_bp.route("/refresh", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    """
    Refresh the access token.
    
    Returns:
        200: New access token
    """
    current_user = get_jwt_identity()
    new_token = AuthService.refresh_access_token(current_user)
    
    return jsonify({"access_token": new_token}), 200
