from app.extensions import db
from app.models.user import Users
from app.user import userBP
from flask import jsonify, request


@userBP.route("/", methods=["GET"], strict_slashes=False)
def get_all_user():
    limit = request.args.get("limit", 10)
    if type(limit) is not int:
        return jsonify({"message": "Invalid Parameter"}), 422

    users = db.session.execute(db.select(Users).limit(limit)).scalars()

    results = []
    for user in users:
        results.append(user.serialize())

    response = jsonify({"success": True, "data": results})

    return response, 200


@userBP.route("/", methods=["POST"], strict_slashes=False)
def create_user():
    data = request.get_json()
    input_username = data.get("username")
    input_email = data.get("email")
    input_password = data.get("password")

    if not input_username or not input_email or not input_password:
        return jsonify({"message": "Data is not complete"}), 422

    new_user = Users(
        username=input_username, email=input_email, password=input_password
    )  # type: ignore

    db.session.add(new_user)
    db.session.commit()

    response = jsonify(
        {
            "success": True,
            "data": new_user.serialize(),
            "message": "Account succesfuly created",
        }
    )

    return response, 201


@userBP.route("/<int:id>", methods=["GET"], strict_slashes=False)
def get_user_by_id(id):
    user = Users.query.filter_by(id=id).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    else:
        response = jsonify({"success": True, "data": user.serialize()})

    return response, 200


@userBP.route("/<int:id>", methods=["PUT"], strict_slashes=False)
def update_user(id):
    data = request.get_json()
    input_username = data.get("username")
    input_email = data.get("email")
    input_password = data.get("password")

    user = Users.query.filter_by(id=id).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    elif not input_username or not input_email or not input_password:
        return jsonify({"succes": False, "message": "Data not complete"}), 422

    else:
        user.username = input_username
        user.email = input_email
        user.password = input_password

    db.session.commit()

    response = jsonify(
        {
            "success": True,
            "message": "Data successfully updated",
            "data": user.basic_serialize(),
        }
    )

    return response, 201


@userBP.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete_user(id):
    user = Users.query.filter_by(id=id).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    else:
        db.session.delete(user)
        db.session.commit()

    response = jsonify({"success": True, "message": "User successfully deleted"})

    return response, 201
