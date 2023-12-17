from app.extensions import db
from app.models.user import Users
from app.user import userBP
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound


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
        # Query user by ID or return a 404 Not Found response
        user = Users.query.get_or_404(user_id)
        response = jsonify({"success": True, "data": user.serialize()})
        return response, 200
    except NoResultFound:
        # Return a 404 Not Found response if the user is not found
        return jsonify({"success": False, "message": "User not found"}), 404


@userBP.route("/", methods=["POST"], strict_slashes=False)
def create_user():
    # Extract data from JSON request
    data = request.get_json()
    input_username, input_email, input_password = (
        data.get("username"),
        data.get("email"),
        data.get("password"),
    )

    # Validate input data
    if not all((input_username, input_email, input_password)):
        # Return a 422 Unprocessable Entity response for incomplete data
        return jsonify({"error": "Incomplete data"}), 422

    # Check email uniqueness before adding to the session
    if is_email_taken(input_email):
        # Return a 422 Unprocessable Entity response for existing email
        return jsonify({"error": "Email already exists"}), 422

    try:
        # Create a new user and add to the session
        new_user = Users(
            username=input_username, email=input_email, password=input_password
        )  # type: ignore
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        # Handle email uniqueness constraint violation with a rollback
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 422

    # Return success response with the newly created user data
    response = jsonify(
        {
            "success": True,
            "data": new_user.serialize(),
            "message": "Account successfully created",
        }
    )

    return response, 201


def is_email_taken(email):
    """Check if the given email is already taken."""
    return Users.query.filter_by(email=email).first() is not None


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


def update_user_object(user, username, email, password):
    # Update user properties with new values
    user.username = username
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
