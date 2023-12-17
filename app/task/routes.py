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


@taskBP.route("/<int:id>", methods=["GET"], strict_slashes=False)
def get_task_by_id(id):
    task = Tasks.query.filter_by(id=id).first()

    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    else:
        response = jsonify({"success": True, "data": task.serialize()})

    return response, 200


@taskBP.route("/<int:id>", methods=["PUT"], strict_slashes=False)
def update_task(id):
    data = request.get_json()
    input_task = data.get("task_name")
    input_description = data.get("description")
    input_due_date = data.get("due_date")
    input_status = data.get("status")
    input_project_id = data.get("project_id")

    task = Tasks.query.filter_by(id=id).first()

    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    elif (
        not input_task
        or not input_description
        or not input_due_date
        or not input_status
        or not input_project_id
    ):
        return jsonify({"success": False, "message": "Data not complete"}), 422

    else:
        task.task_name = input_task
        task.description = input_description
        task.due_date = input_due_date
        task.status = input_status
        task.project_id = input_project_id

    db.session.commit()

    response = jsonify(
        {
            "success": True,
            "message": "task successfully updated",
            "data": task.basic_serialize(),
        }
    )

    return response, 201


@taskBP.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete_task(id):
    task = Tasks.query.filter_by(id=id).first()

    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    response = jsonify({"success": True, "message": "Task successfully deleted"})

    return response, 201
