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


@taskBP.route("/", methods=["POST"], strict_slashes=False)
def cretae_task():
    data = request.get_json()
    input_task = data.get("task_name")
    input_description = data.get("description")
    input_due_date = data.get("due_date")
    input_status = data.get("status")
    input_project_id = data.get("project_id")

    if (
        not input_task
        or not input_description
        or not input_due_date
        or not input_status
        or not input_project_id
    ):
        return jsonify({"message": "Invalid parameter"}), 422

    new_task = Tasks(
        task_name=input_task,
        description=input_description,
        due_date=input_due_date,
        status=input_status,
        project_id=input_project_id,
    )  # type: ignore

    db.session.add(new_task)
    db.session.commit()

    response = jsonify(
        {
            "success": True,
            "data": new_task.serialize(),
            "message": "Task successfully created",
        }
    )

    return response, 201
