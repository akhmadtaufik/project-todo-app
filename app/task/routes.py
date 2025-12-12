from datetime import datetime

from app.extensions import db
from app.models.project import Projects
from app.models.task import Tasks
from app.task import taskBP
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError


def generate_response(success, message, data=None, status_code=200):
    """
    Helper function to generate a consistent response format.
    """
    response_data = {"success": success, "message": message}
    if data is not None:
        response_data["data"] = data
    return jsonify(response_data), status_code


def has_permission(project_id, user_id):
    """Check if the user has permission to access a specific project."""
    project = Projects.query.filter_by(id=project_id, user_id=user_id).first()
    return project is not None


def is_valid_project(project_id, user_id):
    """Check if a project exists and belongs to the user."""
    project = Projects.query.filter_by(id=project_id, user_id=user_id).first()
    return project is not None


@taskBP.route("/<int:project_id>/tasks", methods=["GET"], strict_slashes=False)
@jwt_required(locations=["headers"])
def get_all_task_by_project_id(project_id):
    try:
        current_user = get_jwt_identity()

        if not has_permission(project_id, current_user):
            return generate_response(
                success=False,
                message="You do not have permission to retrieve these tasks",
                status_code=403,
            )

        tasks = db.session.execute(
            db.select(Tasks)
            .join(Projects, Tasks.project_id == Projects.id)
            .filter(Tasks.project_id == project_id)
            .order_by(Tasks.id)
        ).scalars()

        data = [task.serialize() for task in tasks]

        response = generate_response(
            success=True,
            message="Tasks retrieved successfully",
            data=data,
            status_code=200,
        )
        return response

    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(
            False, f"Error retrieving tasks: {str(e)}", status_code=500
        )


@taskBP.route("/task", methods=["POST"], strict_slashes=False)
@jwt_required(locations=["headers"])
def create_task():
    try:
        current_user = get_jwt_identity()

        data = request.get_json()
        input_task = data.get("task_name")
        input_description = data.get("description")
        input_due_date = data.get("due_date")
        input_status = data.get("status")
        input_project_id = data.get("project_id")

        # Check if the project belongs to the authenticated user
        if not is_valid_project(input_project_id, current_user):
            return generate_response(
                success=False,
                message="Invalid project_id for creating a task",
                status_code=403,
            )

        if not all(
            (
                input_task,
                input_description,
                input_due_date,
                input_status,
                input_project_id,
            )
        ):
            return generate_response(
                success=False,
                message="Invalid parameters for creating a task",
                status_code=422,
            )

        # Date Validation: Check if due_date is not earlier than current date
        current_date = datetime.now().date()
        input_due_date = datetime.strptime(input_due_date, "%Y-%m-%d").date()

        if input_due_date < current_date:
            return generate_response(
                success=False,
                message="Due date must be later than the current date",
                status_code=422,
            )

        new_task = Tasks(
            task_name=input_task,
            description=input_description,
            due_date=input_due_date,
            status=input_status,
            project_id=input_project_id,
        )  # type: ignore
        db.session.add(new_task)
        db.session.commit()

        return generate_response(
            success=True,
            message="Task successfully created",
            data=new_task.serialize(),
            status_code=201,
        )
    except SQLAlchemyError as e:
        db.session.rollback()
        return generate_response(
            False, f"Error creating task: {str(e)}", status_code=500
        )


@taskBP.route(
    "/<int:project_id>/task/<int:task_id>", methods=["PUT"], strict_slashes=False
)
@jwt_required(locations=["headers"])
def update_task(project_id, task_id):
    try:
        current_user = get_jwt_identity()

        if not has_permission(current_user):
            return generate_response(
                success=False,
                message="You do not have permission to update tasks",
                status_code=403,
            )

        if not is_valid_project(project_id, current_user):
            return generate_response(
                success=False,
                message="Invalid project_id for updating a task",
                status_code=403,
            )

        task = Tasks.query.filter_by(id=task_id).first()

        if not task:
            return generate_response(
                success=False, message="Task not found", status_code=404
            )

        data = request.get_json()
        input_task = data.get("task_name")
        input_description = data.get("description")
        input_due_date = data.get("due_date")
        input_status = data.get("status")

        if not all(
            (
                input_task,
                input_description,
                input_due_date,
                input_status,
            )
        ):
            return generate_response(False, "Data not complete"), 422

        task.task_name = input_task
        task.description = input_description
        task.due_date = input_due_date
        task.status = input_status
        task.project_id = project_id

        db.session.commit()

        return generate_response(
            success=True,
            message="Task successfully updated",
            data=task.basic_serialize(),
            status_code=201,
        )
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(False, f"Error updating task: {str(e)}"), 500


@taskBP.route(
    "/<int:project_id>/task/<int:task_id>", methods=["DELETE"], strict_slashes=False
)
@jwt_required(locations=["headers"])
def delete_task(project_id, task_id):
    try:
        current_user = get_jwt_identity()

        if not has_permission(current_user):
            return generate_response(
                success=False,
                message="You do not have permission to delete tasks",
                status_code=403,
            )

        if not is_valid_project(project_id, current_user):
            return generate_response(
                success=False,
                message="Invalid project_id for deleting a task",
                status_code=403,
            )

        task = Tasks.query.filter_by(id=task_id, project_id=project_id).first()

        if not task:
            return generate_response(
                success=False, message="Task Not Found", status_code=404
            )

        db.session.delete(task)
        db.session.commit()

        response = generate_response(
            success=True, message="Task successfully deleted", status_code=204
        )

        return response

    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(False, f"Error deleting task: {str(e)}"), 500
