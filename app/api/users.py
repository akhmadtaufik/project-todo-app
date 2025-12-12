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
    Get all users (paginated)
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        schema:
          type: integer
          default: 1
          minimum: 1
        description: Page number (1-indexed)
      - name: per_page
        in: query
        schema:
          type: integer
          default: 10
          minimum: 1
          maximum: 100
        description: Number of items per page
    responses:
      200:
        description: List of users retrieved successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      user_id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: John Doe
                      email:
                        type: string
                        example: john@example.com
                meta:
                  type: object
                  properties:
                    page:
                      type: integer
                      example: 1
                    per_page:
                      type: integer
                      example: 10
                    total_pages:
                      type: integer
                      example: 5
                    total_items:
                      type: integer
                      example: 50
      401:
        description: Missing or invalid token
      422:
        description: Invalid pagination parameter
    """
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
    except ValueError:
        return jsonify({"success": False, "error": "Invalid pagination parameter"}), 422

    result = UserService.get_all_users(page, per_page)
    return jsonify({
        "success": True,
        "data": result["data"],
        "meta": result["meta"]
    }), 200


@users_bp.route("/<int:user_id>", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_user_by_id(user_id):
    """
    Get a user by ID
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: integer
        description: The user ID
    responses:
      200:
        description: User data retrieved successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: John Doe
                    email:
                      type: string
                      example: john@example.com
                    projects:
                      type: array
                      items:
                        type: object
                        properties:
                          project_id:
                            type: integer
                          project_name:
                            type: string
      401:
        description: Missing or invalid token
      403:
        description: No permission to access this user's data
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: You don't have permission to access this user's data
      404:
        description: User not found
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
    Update a user's information
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: integer
        description: The user ID to update
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - email
              - password
            properties:
              username:
                type: string
                example: johndoe
              email:
                type: string
                format: email
                example: john@example.com
              password:
                type: string
                example: NewSecurePass123
    responses:
      200:
        description: User updated successfully
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
                  example: Data successfully updated
                data:
                  type: object
                  properties:
                    id:
                      type: integer
                    name:
                      type: string
                    email:
                      type: string
      401:
        description: Missing or invalid token
      403:
        description: No permission to update this user's data
      404:
        description: User not found
      422:
        description: Incomplete data
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
    Delete a user
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    parameters:
      - name: user_id
        in: path
        required: true
        schema:
          type: integer
        description: The user ID to delete
    responses:
      204:
        description: User deleted successfully
      401:
        description: Missing or invalid token
      403:
        description: No permission to delete this user's account
      404:
        description: User not found
      500:
        description: Database error
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

