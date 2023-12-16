from flask import Blueprint
from werkzeug.exceptions import abort

taskBP = Blueprint("task", __name__)

from app.task import routes
