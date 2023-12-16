from flask import Blueprint
from werkzeug.exceptions import abort

projectBP = Blueprint("project", __name__)

from app.project import routes
