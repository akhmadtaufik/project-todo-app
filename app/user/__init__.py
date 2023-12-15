from flask import Blueprint
from werkzeug.exceptions import abort

userBP = Blueprint("user", __name__)

from app.user import routes
