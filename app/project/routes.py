from app.extensions import db
from app.models.project import Projects
from app.models.user import Users
from app.project import projectBP
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError


def generate_response(success, message, data=None, status_code=200):
    response_data = {"success": success, "message": message}
    if data is not None:
        response_data["data"] = data
    return jsonify(response_data), status_code


@projectBP.route("/", methods=["GET"], strict_slashes=False)
@jwt_required(locations=["headers"])
def get_all_project():
    try:
        # Try to retrieve projects from the database
        user_id = get_jwt_identity()
        limit = int(request.args.get("limit", 10))

        projects = Projects.query.filter_by(user_id=user_id).limit(limit).all()

        results = [project.serialize() for project in projects]

        return generate_response(True, "Projects retrieved successfully", results, 200)
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(
            False, f"Error retrieving projects: {str(e)}", status_code=500
        )


@projectBP.route("/", methods=["POST"], strict_slashes=False)
@jwt_required(locations=["headers"])
def create_project():
    try:
        # Try to create a new project in the database
        data = request.get_json()

        input_project = data.get("project_name")
        input_description = data.get("description")
        input_user_id = get_jwt_identity()

        if not all((input_project, input_description, input_user_id)):
            return generate_response(
                False,
                "Invalid parameters for creating a project.",
                status_code=422,
            )

        new_project = Projects(
            project_name=input_project,
            description=input_description,
            user_id=input_user_id,
        )  # type: ignore
        db.session.add(new_project)
        db.session.commit()

        return generate_response(
            True, "Project successfully created", new_project.serialize(), 201
        )
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(
            False, f"Error creating project: {str(e)}", status_code=500
        )


@projectBP.route("/<int:id>", methods=["GET"], strict_slashes=False)
@jwt_required(locations=["headers"])
def get_project_by_id(id):
    try:
        # Try to retrieve a specific project by ID
        project = Projects.query.get_or_404(id)
        return generate_response(
            True, "Project retrieved successfully", project.serialize()
        )
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(
            False, f"Error retrieving project: {str(e)}", status_code=500
        )


@projectBP.route("/<int:id>", methods=["PUT"], strict_slashes=False)
@jwt_required(locations=["headers"])
def update_project(id):
    try:
        # Try to update a specific project by ID
        current_user = get_jwt_identity()

        project = Projects.query.filter_by(id=id).first()

        if not project:
            return generate_response(
                False,
                "Project not found. Please verify the project ID exists.",
                status_code=404,
            )

        if current_user != str(project.user_id):
            return generate_response(
                False,
                "You do not have permission to edit this project",
                status_code=403,
            )

        data = request.get_json()

        input_project = data.get("project_name")
        input_description = data.get("description")

        if not input_project or not input_description:
            return generate_response(
                False,
                "Incomplete data. Please provide all required fields.",
                status_code=422,
            )
        else:
            project.project_name = input_project
            project.description = input_description

        db.session.commit()

        return generate_response(
            True,
            "Project successfully updated",
            project.basic_serialize(),
            status_code=201,
        )
    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(
            False, f"Error updating project: {str(e)}", status_code=500
        )


@projectBP.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
@jwt_required(locations=["headers"])
def delete_project(id):
    try:
        # Try to delete a specific project by ID
        current_user = get_jwt_identity()

        project = Projects.query.get_or_404(id)

        if current_user != str(project.user_id):
            return generate_response(
                False,
                "You do not have permission to edit this project",
                status_code=403,
            )

        db.session.delete(project)
        db.session.commit()

        return generate_response(True, "Project successfully deleted", status_code=204)

    except SQLAlchemyError as e:
        # Handle database error, rollback, and return an error response
        db.session.rollback()
        return generate_response(
            False, f"Error deleting project: {str(e)}", status_code=500
        )
