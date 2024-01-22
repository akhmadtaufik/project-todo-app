from flask import Blueprint
from flask_cors import CORS
from werkzeug.exceptions import abort

userBP = Blueprint("user", __name__)
CORS(userBP)

from app.user import routes
