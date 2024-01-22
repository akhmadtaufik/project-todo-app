from flask import Blueprint
from flask_cors import CORS
from werkzeug.exceptions import abort

frontendBP = Blueprint("frontend", __name__)
CORS(frontendBP)

from app.frontend import routes
