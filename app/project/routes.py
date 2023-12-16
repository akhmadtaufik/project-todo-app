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
