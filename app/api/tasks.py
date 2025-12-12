"""
Tasks API Routes

Handles task CRUD operations.
"""
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

from app.api import tasks_bp
from app.services.task_service import TaskService
from app.common.response_util import generate_response


@tasks_bp.route("/<int:project_id>/tasks", methods=["GET"], strict_slashes=False)
@jwt_required(locations=["headers"])
def get_all_tasks_by_project_id(project_id):
    """
    Get all tasks for a project
    ---
    tags:
      - Tasks
    security:
      - BearerAuth: []
    parameters:
      - name: project_id
        in: path
        required: true
        schema:
          type: integer
        description: The project ID to get tasks for
    responses:
      200:
        description: List of tasks retrieved successfully
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
                  example: Tasks retrieved successfully
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      task_id:
                        type: integer
                        example: 1
                      task_name:
                        type: string
                        example: Complete documentation
                      description:
                        type: string
                        example: Write API documentation
                      due_date:
                        type: string
                        format: date
                        example: "2025-12-31"
                      status:
                        type: string
                        example: pending
                      project_id:
                        type: integer
                        example: 1
                      created_at:
                        type: string
                        format: date-time
                      update_at:
                        type: string
                        format: date-time
      401:
        description: Missing or invalid token
      403:
        description: No permission to retrieve these tasks
      500:
        description: Database error
    """
    try:
        current_user = get_jwt_identity()
        
        if not TaskService.has_permission(project_id, current_user):
            return generate_response(
                False, "You do not have permission to retrieve these tasks",
                status_code=403
            )
        
        tasks = TaskService.get_tasks_by_project(project_id)
        
        return generate_response(True, "Tasks retrieved successfully", tasks, 200)
    except SQLAlchemyError as e:
        return generate_response(False, f"Error retrieving tasks: {str(e)}", status_code=500)


@tasks_bp.route("/task", methods=["POST"], strict_slashes=False)
@jwt_required(locations=["headers"])
def create_task():
    """
    Create a new task
    ---
    tags:
      - Tasks
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - task_name
              - description
              - due_date
              - status
              - project_id
            properties:
              task_name:
                type: string
                example: Complete documentation
              description:
                type: string
                example: Write API documentation for all endpoints
              due_date:
                type: string
                format: date
                description: Due date in YYYY-MM-DD format (must be in the future)
                example: "2025-12-31"
              status:
                type: string
                enum: [pending, in_progress, completed]
                example: pending
              project_id:
                type: integer
                description: The project ID this task belongs to
                example: 1
    responses:
      201:
        description: Task created successfully
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
                  example: Task created successfully
                data:
                  type: object
                  properties:
                    task_id:
                      type: integer
                      example: 1
                    task_name:
                      type: string
                    description:
                      type: string
                    due_date:
                      type: string
                      format: date
                    status:
                      type: string
                    project_id:
                      type: integer
                    created_at:
                      type: string
                      format: date-time
      401:
        description: Missing or invalid token
      403:
        description: Invalid project_id for creating a task
      422:
        description: Invalid parameters or due date in the past
      500:
        description: Database error
    """
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        
        task_name = data.get("task_name")
        description = data.get("description")
        due_date_str = data.get("due_date")
        status = data.get("status")
        project_id = data.get("project_id")
        
        # Check project ownership
        if not TaskService.is_valid_project(project_id, current_user):
            return generate_response(
                False, "Invalid project_id for creating a task",
                status_code=403
            )
        
        # Validate required fields
        if not all((task_name, description, due_date_str, status, project_id)):
            return generate_response(
                False, "Invalid parameters for creating a task",
                status_code=422
            )
        
        # Validate due date
        is_valid, message, due_date = TaskService.validate_due_date(due_date_str)
        if not is_valid:
            return generate_response(False, message, status_code=422)
        
        success, message, task_data = TaskService.create_task(
            task_name, description, due_date, status, project_id
        )
        
        if success:
            return generate_response(True, message, task_data, 201)
        else:
            return generate_response(False, message, status_code=500)
    except SQLAlchemyError as e:
        return generate_response(False, f"Error creating task: {str(e)}", status_code=500)


@tasks_bp.route("/<int:project_id>/task/<int:task_id>", methods=["PUT"], strict_slashes=False)
@jwt_required(locations=["headers"])
def update_task(project_id, task_id):
    """
    Update a task
    ---
    tags:
      - Tasks
    security:
      - BearerAuth: []
    parameters:
      - name: project_id
        in: path
        required: true
        schema:
          type: integer
        description: The project ID the task belongs to
      - name: task_id
        in: path
        required: true
        schema:
          type: integer
        description: The task ID to update
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - task_name
              - description
              - due_date
              - status
            properties:
              task_name:
                type: string
                example: Updated task name
              description:
                type: string
                example: Updated task description
              due_date:
                type: string
                format: date
                example: "2025-12-31"
              status:
                type: string
                enum: [pending, in_progress, completed]
                example: in_progress
    responses:
      201:
        description: Task updated successfully
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
                  example: Task updated successfully
                data:
                  type: object
                  properties:
                    task_name:
                      type: string
                    description:
                      type: string
                    due_date:
                      type: string
                      format: date
                    status:
                      type: string
                    update_at:
                      type: string
                      format: date-time
      401:
        description: Missing or invalid token
      403:
        description: No permission or invalid project
      404:
        description: Task not found
      422:
        description: Incomplete data
      500:
        description: Database error
    """
    try:
        current_user = get_jwt_identity()
        
        if not TaskService.is_valid_project(project_id, current_user):
            return generate_response(
                False, "Invalid project_id for updating a task",
                status_code=403
            )
        
        task = TaskService.get_task_by_id(task_id)
        
        if not task:
            return generate_response(False, "Task not found", status_code=404)
        
        data = request.get_json()
        task_name = data.get("task_name")
        description = data.get("description")
        due_date = data.get("due_date")
        status = data.get("status")
        
        if not all((task_name, description, due_date, status)):
            return generate_response(False, "Data not complete", status_code=422)
        
        success, message, task_data = TaskService.update_task(
            task, task_name, description, due_date, status, project_id
        )
        
        if success:
            return generate_response(True, message, task_data, 201)
        else:
            return generate_response(False, message, status_code=500)
    except SQLAlchemyError as e:
        return generate_response(False, f"Error updating task: {str(e)}", status_code=500)


@tasks_bp.route("/<int:project_id>/task/<int:task_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required(locations=["headers"])
def delete_task(project_id, task_id):
    """
    Delete a task
    ---
    tags:
      - Tasks
    security:
      - BearerAuth: []
    parameters:
      - name: project_id
        in: path
        required: true
        schema:
          type: integer
        description: The project ID the task belongs to
      - name: task_id
        in: path
        required: true
        schema:
          type: integer
        description: The task ID to delete
    responses:
      204:
        description: Task deleted successfully
      401:
        description: Missing or invalid token
      403:
        description: No permission or invalid project
      404:
        description: Task not found
      500:
        description: Database error
    """
    try:
        current_user = get_jwt_identity()
        
        if not TaskService.is_valid_project(project_id, current_user):
            return generate_response(
                False, "Invalid project_id for deleting a task",
                status_code=403
            )
        
        task = TaskService.get_task_by_id_and_project(task_id, project_id)
        
        if not task:
            return generate_response(False, "Task Not Found", status_code=404)
        
        success, message = TaskService.delete_task(task)
        
        if success:
            return generate_response(True, message, status_code=204)
        else:
            return generate_response(False, message, status_code=500)
    except SQLAlchemyError as e:
        return generate_response(False, f"Error deleting task: {str(e)}", status_code=500)

