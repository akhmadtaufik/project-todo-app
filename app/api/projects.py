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
    Get all projects for the current user
    ---
    tags:
      - Projects
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
        description: List of projects retrieved successfully
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
                  example: Projects retrieved successfully
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      project_id:
                        type: integer
                        example: 1
                      project_name:
                        type: string
                        example: My First Project
                      description:
                        type: string
                        example: A sample project
                      user_id:
                        type: integer
                        example: 1
                      created_at:
                        type: string
                        format: date-time
                      update_at:
                        type: string
                        format: date-time
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
      500:
        description: Database error
    """
    try:
        user_id = get_jwt_identity()
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        
        result = ProjectService.get_user_projects(user_id, page, per_page)
        
        return jsonify({
            "success": True,
            "message": "Projects retrieved successfully",
            "data": result["data"],
            "meta": result["meta"]
        }), 200
    except SQLAlchemyError as e:
        return generate_response(False, f"Error retrieving projects: {str(e)}", status_code=500)


@projects_bp.route("/", methods=["POST"], strict_slashes=False)
@jwt_required(locations=["headers"])
def create_project():
    """
    Create a new project
    ---
    tags:
      - Projects
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - project_name
            properties:
              project_name:
                type: string
                example: My New Project
              description:
                type: string
                example: Description of the project
    responses:
      201:
        description: Project created successfully
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
                  example: Project created successfully
                data:
                  type: object
                  properties:
                    project_id:
                      type: integer
                      example: 1
                    project_name:
                      type: string
                      example: My New Project
                    description:
                      type: string
                    user_id:
                      type: integer
                    created_at:
                      type: string
                      format: date-time
      401:
        description: Missing or invalid token
      422:
        description: Invalid parameters
      500:
        description: Database error
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
    Get a project by ID
    ---
    tags:
      - Projects
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: The project ID
    responses:
      200:
        description: Project retrieved successfully
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
                  example: Project retrieved successfully
                data:
                  type: object
                  properties:
                    project_id:
                      type: integer
                    project_name:
                      type: string
                    description:
                      type: string
                    user_id:
                      type: integer
                    created_at:
                      type: string
                      format: date-time
                    update_at:
                      type: string
                      format: date-time
      401:
        description: Missing or invalid token
      404:
        description: Project not found
      500:
        description: Database error
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
    Update a project
    ---
    tags:
      - Projects
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: The project ID to update
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - project_name
            properties:
              project_name:
                type: string
                example: Updated Project Name
              description:
                type: string
                example: Updated project description
    responses:
      201:
        description: Project updated successfully
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
                  example: Project updated successfully
                data:
                  type: object
                  properties:
                    project_name:
                      type: string
                    description:
                      type: string
                    update_at:
                      type: string
                      format: date-time
      401:
        description: Missing or invalid token
      403:
        description: No permission to edit this project
      404:
        description: Project not found
      422:
        description: Incomplete data
      500:
        description: Database error
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
    Delete a project
    ---
    tags:
      - Projects
    security:
      - BearerAuth: []
    parameters:
      - name: id
        in: path
        required: true
        schema:
          type: integer
        description: The project ID to delete
    responses:
      204:
        description: Project deleted successfully
      401:
        description: Missing or invalid token
      403:
        description: No permission to delete this project
      404:
        description: Project not found
      500:
        description: Database error
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

