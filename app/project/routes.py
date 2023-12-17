from app.extensions import db
from app.models.project import Projects
from app.models.user import Users
from app.project import projectBP
from flask import jsonify, request


@projectBP.route("/", methods=["GET"], strict_slashes=False)
def get_all_project():
    limit = request.args.get("limit", 10)
    if type(limit) is not int:
        return jsonify({"message": "Invalid paramater"}), 422

    projects = db.session.execute(db.select(Projects).limit(limit)).scalars()

    results = [project.serialize() for project in projects]

    response = jsonify({"success": True, "data": results})

    return response, 200


@projectBP.route("/", methods=["POST"], strict_slashes=False)
def cretae_project():
    data = request.get_json()
    input_project = data.get("project_name")
    input_description = data.get("description")
    input_user_id = data.get("user_id")

    if not input_project or not input_description or not input_user_id:
        return jsonify({"message": "Invalid Parameter"})

    new_project = Projects(
        project_name=input_project, description=input_description, user_id=input_user_id
    )  # type: ignore

    db.session.add(new_project)
    db.session.commit()

    response = jsonify(
        {
            "success": True,
            "data": new_project.serialize(),
            "message": "Project successfully created",
        }
    )

    return response, 201


@projectBP.route("/<int:id>", methods=["GET"], strict_slashes=False)
def get_project_by_id(id):
    project = Projects.query.filter_by(id=id).first()

    if not project:
        return jsonify({"success": False, "message": "Project not found"}), 404

    else:
        response = jsonify({"success": True, "data": project.serialize()})

    return response, 200


@projectBP.route("/<int:id>", methods=["PUT"], strict_slashes=False)
def update_project(id):
    data = request.get_json()
    input_project = data.get("project_name")
    input_description = data.get("description")
    input_user_id = data.get("user_id")

    project = Projects.query.filter_by(id=id).first()

    if not project:
        return jsonify({"success": False, "message": "Project not found"}), 404

    elif not input_project or not input_description or not input_user_id:
        return jsonify({"success": False, "message": "Data not complete"}), 422

    else:
        project.project_name = input_project
        project.description = input_description
        project.user_id = input_user_id

    db.session.commit()

    response = jsonify(
        {
            "success": True,
            "message": "Project successfully updated",
            "data": project.basic_serialize(),
        }
    )

    return response, 201


@projectBP.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete_project(id):
    project = Projects.query.filter_by(id=id).first()

    if not project:
        return jsonify({"success": False, "message": "Project not found"}), 404

    db.session.delete(project)
    db.session.commit()

    response = jsonify({"success": True, "message": "Project successfully deleted"})

    return response, 201
