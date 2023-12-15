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
