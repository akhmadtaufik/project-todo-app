from flask import Blueprint
from flask_cors import CORS
from werkzeug.exceptions import abort

taskBP = Blueprint("task", __name__)
CORS(taskBP)

from app.task import routes
