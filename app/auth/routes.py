from app.auth import authBP
from app.extensions import db, jwt
from app.models.user import Users
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash


@authBP.route("/register", methods=["POST"], strict_slashes=False)
def registration():
    """
    Register a new user.

    This route handles user registration by receiving user data, validating it, and storing it in the database.

    Args:
        None

    Returns:
        response (tuple): A tuple containing the response object and the status code.
            - Success: A response with status code 201 and a message indicating successful registration.
            - Error: A response with status code 422 and a message indicating incomplete data or a duplicate email.
    """
    data = request.get_json()

    input_name = data.get("name")
    input_email = data.get("email")
    input_password = generate_password_hash(data.get("password", None))

    if not input_name or not input_email or not input_password:
        return (
            jsonify(
                {"message": "Incomplete data. Please provide all required fields."}
            ),
            422,
        )

    try:
        db.session.add(
            Users(name=input_name, email=input_email, password=input_password)  # type: ignore
        )
        db.session.commit()
    except IntegrityError:
        return jsonify({"message": f"Email '{input_email}' is already registered."})

    response = jsonify({"message": "Registration user is completed"})

    return response, 201


@authBP.route("/login", methods=["POST"], strict_slashes=False)
def login():
    """
    Login with user credentials.

    This route handles user login by verifying the user's credentials and generating access and refresh tokens.

    Args:
        None

    Returns:
        response (tuple): A tuple containing the response object and the status code.
            - Success: A response with status code 200 and access and refresh tokens.
            - Error: A response with status code 400 or 401 and an error message indicating incomplete data or invalid credentials.
    """
    data = request.get_json()

    input_username = data.get("email")
    input_password = data.get("password")

    if not input_username or not input_password:
        return (
            jsonify(
                {"message": "Incomplete data. Please provide all required fields."}
            ),
            400,
        )

    user = Users.query.filter_by(email=input_username).first()
    if not user:
        return jsonify({"message": "User not found"}), 400

    is_valid = check_password_hash(user.password, input_password)

    if not is_valid:
        return (
            jsonify({"message": "Invalid credentials. Check your password."}),
            401,
        )

    else:
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

    response = jsonify(
        {
            "message": "Login successfully",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    )

    return response, 200


@authBP.route("/refresh", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    """
    Refresh the access token.

    This route refreshes the access token for an authenticated user.

    Args:
        None

    Returns:
        response (tuple): A tuple containing the response object and the status code.
            - Success: A response with status code 200 and a new access token.
            - Error: A response with status code 401 if the refresh token is invalid or expired.
    """
    current_user = get_jwt_identity()
    new_token = {"access_token": create_access_token(identity=current_user)}

    return jsonify(new_token), 200
