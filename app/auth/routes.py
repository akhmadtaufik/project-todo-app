from app.auth import authBP
from app.extensions import db, jwt
from app.models.project import Projects
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
    current_user = get_jwt_identity()
    new_token = {"access_token": create_access_token(identity=current_user)}

    return jsonify(new_token), 200
