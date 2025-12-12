"""
Users API Routes

Handles user CRUD operations.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from app.api import users_bp
from app.services.user_service import UserService
from app.common.response_util import success_response, error_response


@users_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_all_users():
    """
    Retrieves a limited number of user records.
    
    Returns:
        200: List of users
        422: Invalid parameter
    """
    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"error": "Invalid parameter"}), 422

    users = UserService.get_all_users(limit)
    return jsonify({"success": True, "data": users}), 200


@users_bp.route("/<int:user_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_user_by_id(user_id):
    """
    Retrieves a user by ID.
    
    Returns:
        200: User data
        403: No permission
        404: User not found
    """
    current_user_id = get_jwt_identity()
    
    if not UserService.check_user_permission(current_user_id, user_id):
        return jsonify({"error": "You don't have permission to access this user's data"}), 403

    try:
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        data = UserService.serialize_user_with_projects(user)
        return jsonify({"success": True, "data": data}), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@users_bp.route("/<int:user_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_user(user_id):
    """
    Update a user's information.
    
    Returns:
        200: Updated user data
        403: No permission
        404: User not found
        422: Incomplete data
    """
    current_user_id = get_jwt_identity()
    
    if not UserService.check_user_permission(current_user_id, user_id):
        return jsonify({"error": "You don't have permission to update this user's data"}), 403

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not all((username, email, password)):
            return jsonify({"error": "Data not complete"}), 422

        updated_user = UserService.update_user(user, username, email, password)
        
        return jsonify({
            "success": True,
            "message": "Data successfully updated",
            "data": UserService.serialize_user_basic(updated_user)
        }), 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@users_bp.route("/<int:user_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def delete_user(user_id):
    """
    Delete a user.
    
    Returns:
        204: User deleted
        403: No permission
        500: Database error
    """
    current_user_id = get_jwt_identity()
    
    if not UserService.check_user_permission(current_user_id, user_id):
        return jsonify({"error": "You don't have permission to delete this user's account"}), 403

    try:
        user = UserService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        success, message = UserService.delete_user(user)
        
        if success:
            return jsonify({"success": True, "message": message}), 204
        else:
            return jsonify({"error": message}), 500

    except SQLAlchemyError:
        return jsonify({"error": "Error deleting user"}), 500
