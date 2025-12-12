"""
Projects API Routes

Handles project CRUD operations.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from app.api import projects_bp
from app.services.project_service import ProjectService
from app.common.response_util import generate_response


@projects_bp.route("/", methods=["GET"], strict_slashes=False)
@jwt_required(locations=["headers"])
def get_all_projects():
    """
    Get all projects for the current user.
    
    Returns:
        200: List of projects
        500: Database error
    """
    try:
        user_id = get_jwt_identity()
        limit = int(request.args.get("limit", 10))
        
        projects = ProjectService.get_user_projects(user_id, limit)
        
        return generate_response(True, "Projects retrieved successfully", projects, 200)
    except SQLAlchemyError as e:
        return generate_response(False, f"Error retrieving projects: {str(e)}", status_code=500)


@projects_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required(locations=["headers"])
def create_project():
    """
    Create a new project.
    
    Returns:
        201: Project created
        422: Invalid parameters
        500: Database error
    """
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        project_name = data.get("project_name")
        description = data.get("description")
        
        success, message, project_data = ProjectService.create_project(
            project_name, description, user_id
        )
        
        if success:
            return generate_response(True, message, project_data, 201)
        else:
            return generate_response(False, message, status_code=422)
    except SQLAlchemyError as e:
        return generate_response(False, f"Error creating project: {str(e)}", status_code=500)


@projects_bp.route("/<int:id>", methods=["GET"], strict_slashes=False)
@jwt_required(locations=["headers"])
def get_project_by_id(id):
    """
    Get a project by ID.
    
    Returns:
        200: Project data
        404: Project not found
        500: Database error
    """
    try:
        project = ProjectService.get_project_by_id(id)
        
        if not project:
            return generate_response(False, "Project not found", status_code=404)
        
        return generate_response(
            True, "Project retrieved successfully", 
            ProjectService.serialize_project(project)
        )
    except SQLAlchemyError as e:
        return generate_response(False, f"Error retrieving project: {str(e)}", status_code=500)


@projects_bp.route("/<int:id>", methods=["PUT"], strict_slashes=False)
@jwt_required(locations=["headers"])
def update_project(id):
    """
    Update a project.
    
    Returns:
        201: Project updated
        403: No permission
        404: Project not found
        422: Incomplete data
    """
    try:
        current_user = get_jwt_identity()
        
        project = ProjectService.get_project_by_id(id)
        
        if not project:
            return generate_response(
                False, "Project not found. Please verify the project ID exists.",
                status_code=404
            )
        
        if current_user != str(project.user_id):
            return generate_response(
                False, "You do not have permission to edit this project",
                status_code=403
            )
        
        data = request.get_json()
        project_name = data.get("project_name")
        description = data.get("description")
        
        success, message, project_data = ProjectService.update_project(
            project, project_name, description
        )
        
        if success:
            return generate_response(True, message, project_data, 201)
        else:
            return generate_response(False, message, status_code=422)
    except SQLAlchemyError as e:
        return generate_response(False, f"Error updating project: {str(e)}", status_code=500)


@projects_bp.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
@jwt_required(locations=["headers"])
def delete_project(id):
    """
    Delete a project.
    
    Returns:
        204: Project deleted
        403: No permission
        404: Project not found
    """
    try:
        current_user = get_jwt_identity()
        
        project = ProjectService.get_project_by_id(id)
        
        if not project:
            return generate_response(False, "Project not found", status_code=404)
        
        if current_user != str(project.user_id):
            return generate_response(
                False, "You do not have permission to delete this project",
                status_code=403
            )
        
        success, message = ProjectService.delete_project(project)
        
        if success:
            return generate_response(True, message, status_code=204)
        else:
            return generate_response(False, message, status_code=500)
    except SQLAlchemyError as e:
        return generate_response(False, f"Error deleting project: {str(e)}", status_code=500)
