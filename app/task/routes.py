from app.extensions import db
from app.models.project import Projects
from app.models.task import Tasks
from app.models.user import Users
from app.task import taskBP
from flask import jsonify, request


@taskBP.route("/", methods=["GET"], strict_slashes=False)
def get_all_task():
    limit = request.args.get("limit", 10)

    if type(limit) is not int:
        return jsonify({"message": "Invalid parameter"}), 422

    tasks = db.session.execute(db.select(Tasks).limit(limit)).scalars()

    results = [task.serialize() for task in tasks]

    response = jsonify({"success": True, "data": results})

    return response, 200
