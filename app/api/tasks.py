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
    Get all tasks for a project.
    
    Returns:
        200: List of tasks
        403: No permission
        500: Database error
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
    Create a new task.
    
    Returns:
        201: Task created
        403: Invalid project
        422: Invalid parameters or due date
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
    Update a task.
    
    Returns:
        201: Task updated
        403: No permission or invalid project
        404: Task not found
        422: Incomplete data
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
    Delete a task.
    
    Returns:
        204: Task deleted
        403: No permission or invalid project
        404: Task not found
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
