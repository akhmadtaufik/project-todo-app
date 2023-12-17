from app.extensions import db
from app.models.project import Projects
from app.models.task import Tasks
from app.models.user import Users
from app.task import taskBP
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError


def generate_response(success, message, data=None, status_code=200):
    """
    Helper function to generate a consistent response format.
    """
    response_data = {"success": success, "message": message}
    if data is not None:
        response_data["data"] = data
    return jsonify(response_data), status_code


@taskBP.route("/", methods=["GET"], strict_slashes=False)
def get_all_task():
    try:
        # Try to retrieve tasks from the database
        limit = int(request.args.get("limit", 10))
        tasks = db.session.execute(db.select(Tasks).limit(limit)).scalars()
        results = [task.serialize() for task in tasks]
        return generate_response(True, "Tasks retrieved successfully", results)
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(False, f"Error retrieving tasks: {str(e)}"), 500


@taskBP.route("/", methods=["POST"], strict_slashes=False)
def create_task():
    try:
        # Try to create a new task in the database
        data = request.get_json()
        input_task = data.get("task_name")
        input_description = data.get("description")
        input_due_date = data.get("due_date")
        input_status = data.get("status")
        input_project_id = data.get("project_id")

        if not all(
            (
                input_task,
                input_description,
                input_due_date,
                input_status,
                input_project_id,
            )
        ):
            return (
                generate_response(False, "Invalid parameters for creating a task"),
                422,
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
            True, "Task successfully created", new_task.serialize(), 201
        )
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(False, f"Error creating task: {str(e)}"), 500


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
