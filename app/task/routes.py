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


@taskBP.route("/<int:project_id>/tasks", methods=["GET"], strict_slashes=False)
@jwt_required(locations=["headers"])
def get_all_task_by_project_id(project_id):
    try:
        current_user = get_jwt_identity()

        # Query projects once and store the result
        auth_projects = Projects.query.filter_by(user_id=current_user).all()

        if not auth_projects or current_user != str(auth_projects[0].user_id):
            response = generate_response(
                success=False,
                message="You do not have permission to retrieve these tasks",
                status_code=403,
            )
            return response

        projects = [project.id for project in auth_projects]

        # Check if the project_id is valid
        if project_id not in projects:
            response = generate_response(
                success=False,
                message="Task not found. Please verify the project ID",
                status_code=404,
            )
            return response

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


@taskBP.route("/tasks", methods=["POST"], strict_slashes=False)
@jwt_required(locations=["headers"])
def create_task():
    try:
        current_user = get_jwt_identity()

        auth_projects = Projects.query.filter_by(user_id=current_user).all()

        if not auth_projects or current_user != str(auth_projects[0].user_id):
            response = generate_response(
                success=False,
                message="You do not have permission to create tasks",
                status_code=403,
            )
            return response

        projects = {project.id for project in auth_projects}

        data = request.get_json()
        input_task = data.get("task_name")
        input_description = data.get("description")
        input_due_date = data.get("due_date")
        input_status = data.get("status")
        input_project_id = data.get("project_id")

        if input_project_id not in projects:
            response = generate_response(
                success=False,
                message="Invalid project_id for creating a task",
                status_code=403,
            )
            return response

        if not all(
            (
                input_task,
                input_description,
                input_due_date,
                input_status,
                input_project_id,
            )
        ):
            response = generate_response(
                success=False,
                message="Invalid parameters for creating a task",
                status_code=422,
            )
            return response

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


@taskBP.route("/<int:id>", methods=["GET"], strict_slashes=False)
def get_task_by_id(id):
    try:
        # Try to retrieve a specific task by ID
        task = Tasks.query.get_or_404(id)
        return generate_response(True, "Task retrieved successfully", task.serialize())
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(False, f"Error retrieving task: {str(e)}"), 500


@taskBP.route("/<int:id>", methods=["PUT"], strict_slashes=False)
def update_task(id):
    try:
        # Try to update a specific task by ID
        data = request.get_json()
        input_task = data.get("task_name")
        input_description = data.get("description")
        input_due_date = data.get("due_date")
        input_status = data.get("status")
        input_project_id = data.get("project_id")

        task = Tasks.query.get_or_404(id)

        if not all(
            (
                input_task,
                input_description,
                input_due_date,
                input_status,
                input_project_id,
            )
        ):
            return generate_response(False, "Data not complete"), 422

        task.task_name = input_task
        task.description = input_description
        task.due_date = input_due_date
        task.status = input_status
        task.project_id = input_project_id

        db.session.commit()

        return generate_response(
            True, "Task successfully updated", task.basic_serialize(), 201
        )
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(False, f"Error updating task: {str(e)}"), 500


@taskBP.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete_task(id):
    try:
        # Try to delete a specific task by ID
        task = Tasks.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()

        return generate_response(True, "Task successfully deleted", status_code=204)
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(False, f"Error deleting task: {str(e)}"), 500
