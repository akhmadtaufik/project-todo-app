from flask import Blueprint
from werkzeug.exceptions import abort

authBP = Blueprint("auth", __name__)

from app.auth import routes
