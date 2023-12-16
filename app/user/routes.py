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
