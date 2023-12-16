from app.extensions import db, migrate
from app.project import projectBP
from app.task import taskBP
from app.user import userBP
from config import Config
from flask import Flask


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(userBP, url_prefix="/users")
    app.register_blueprint(projectBP, url_prefix="/projects")
    app.register_blueprint(taskBP, url_prefix="/projects/task")

    return app
