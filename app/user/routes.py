from app.extensions import db
from app.models.user import Users
from app.user import userBP
from flask import jsonify, request
from sqlalchemy.exc import SQLAlchemyError


@userBP.route("/", methods=["GET"], strict_slashes=False)
def get_all_users():
    try:
        # Parse the 'limit' query parameter, default to 10 if not provided
        limit = int(request.args.get("limit", 10))
    except ValueError:
        # Return a 422 Unprocessable Entity response for invalid parameter
        return jsonify({"error": "Invalid parameter"}), 422

    # Query users and serialize the results
    users = db.session.query(Users).limit(limit).all()
    results = [user.serialize() for user in users]

    # Construct a JSON response with the serialized user data
    response = jsonify({"success": True, "data": results})

    return response, 200


@userBP.route("/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    try:
        user = Users.query.get_or_404(user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        response = jsonify({"success": True, "data": user.serialize()})

        return response, 200

    except SQLAlchemyError:
        return jsonify({"error": "Database error"}), 500


@userBP.route("/<int:user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    # Extract JSON data from the request
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:
        # Query the user based on ID or return a 404 Not Found response
        user = Users.query.get_or_404(user_id)
    except SQLAlchemyError:
        # Handle database error with a 500 Internal Server Error response
        return jsonify({"error": "Database error"}), 500

    if not user:
        # If user is not found, return a 404 Not Found response
        return jsonify({"error": "User not found"}), 404

    if not all((username, email, password)):
        # If data is incomplete, return a 422 Unprocessable Entity response
        return jsonify({"error": "Data not complete"}), 422

    # Update the user object with new data and commit the transaction
    update_user_object(user, username, email, password)
    db.session.commit()

    # Construct a JSON response with the newly updated user data
    response = jsonify(
        {
            "success": True,
            "message": "Data successfully updated",
            "data": user.basic_serialize(),
        }
    )

    return response, 200


def update_user_object(user, name, email, password):
    # Update user properties with new values
    user.name = name
    user.email = email
    user.password = password


@userBP.route("/<int:user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    try:
        # Query the user based on ID or return a 404 Not Found response
        user = Users.query.get_or_404(user_id)

        # Delete the user from the database and commit the transaction
        db.session.delete(user)
        db.session.commit()

        # Construct a JSON response for a successful deletion with status code 204 No Content
        response = jsonify({"success": True, "message": "User successfully deleted"})
        return response, 204
    except SQLAlchemyError:
        # Handle database error, perform a rollback, and return a 500 Internal Server Error response
        db.session.rollback()
        return jsonify({"error": "Error deleting user"}), 500
