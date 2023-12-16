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
