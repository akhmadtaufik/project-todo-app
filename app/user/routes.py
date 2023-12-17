from app.extensions import db
from app.models.user import Users
from app.user import userBP
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound


@userBP.route("/", methods=["GET"], strict_slashes=False)
def get_all_user():
    try:
        limit = int(request.args.get("limit", 10))
    except ValueError:
        return jsonify({"message": "Invalid Parameter"}), 422

    users = db.session.query(Users).limit(limit).all()

    results = [user.serialize() for user in users]

    response = jsonify({"success": True, "data": results})

    return response, 200


@userBP.route("/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    try:
        user = Users.query.get_or_404(user_id)
        response = jsonify({"success": True, "data": user.serialize()})
        return response, 200
    except NoResultFound:
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
        return jsonify({"message": "Incomplete data"}), 422

    # Check email uniqueness before adding to the session
    if is_email_taken(input_email):
        return jsonify({"message": "Email already exists"}), 422

    try:
        # Create a new user and add to the session
        new_user = Users(
            username=input_username, email=input_email, password=input_password
        )  # type: ignore
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({"message": "Email already exists"}), 422

    # Return success response
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


@userBP.route("/<int:id>", methods=["PUT"], strict_slashes=False)
def update_user(id):
    # Extract JSON data from the request
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:
        # Query the user based on ID
        user = Users.query.filter_by(id=id).first()
    except SQLAlchemyError:
        # Handle database error
        return jsonify({"success": False, "message": "Database error"}), 500

    if not user:
        # If user is not found, return a 404 response
        return jsonify({"success": False, "message": "User not found"}), 404

    if not all((username, email, password)):
        # If data is incomplete, return a 422 response
        return jsonify({"success": False, "message": "Data not complete"}), 422

    # Update the user object with new data
    update_user_object(user, username, email, password)
    db.session.commit()

    # Construct a JSON response with the newly updated data
    response = jsonify(
        {
            "success": True,
            "message": "Data successfully updated",
            "data": user.basic_serialize(),
        }
    )

    return response, 201


def update_user_object(user, username, email, password):
    # Update user properties with new values
    user.username = username
    user.email = email
    user.password = password


@userBP.route("/<int:id>", methods=["DELETE"], strict_slashes=False)
def delete_user(id):
    try:
        # Query the user based on ID
        user = Users.query.filter_by(id=id).first()

        if not user:
            # If user is not found, return a 404 response
            return jsonify({"success": False, "message": "User not found"}), 404

        # Delete the user from the database and commit the transaction
        db.session.delete(user)
        db.session.commit()

        # Construct a JSON response for a successful deletion with status code 204 No Content
        response = jsonify({"success": True, "message": "User successfully deleted"})
        return response, 204
    except Exception:
        # Handle database error, perform a rollback, and return a 500 response
        db.session.rollback()
        return jsonify({"success": False, "message": "Error deleting user"}), 500
