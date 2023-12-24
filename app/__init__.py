"""
Application Factory Function

This function, create_app, serves as an application factory for Flask.
It creates and configures a Flask application, initializes necessary
extensions, registers blueprints for modular organization, and returns
the configured app.
"""

# Importing necessary components from different modules and packages.
from app.auth import authBP
from app.extensions import db, jwt, migrate
from app.project import projectBP
from app.task import taskBP
from app.user import userBP
from config import Config
from flask import Flask


# Define the create_app function, allowing customization through
# a provided config class.
def create_app(config_class=Config):
    # Create a Flask application.
    app = Flask(__name__)

    # Load configuration settings from the provided config class.
    app.config.from_object(config_class)

    # Initialize Flask extensions: SQLAlchemy, Flask-Migrate,
    # and Flask-JWT-Extended.
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register modular blueprints to organize routes and views.
    app.register_blueprint(authBP, url_prefix="/api/auth")
    app.register_blueprint(userBP, url_prefix="/api/users")
    app.register_blueprint(projectBP, url_prefix="/api/projects")
    app.register_blueprint(taskBP, url_prefix="/api/projects/task")

    # Return the configured app instance.
    return app
