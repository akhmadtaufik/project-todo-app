from flask import Blueprint
from flask_cors import CORS
from werkzeug.exceptions import abort

projectBP = Blueprint("project", __name__)
CORS(projectBP)

from app.project import routes
