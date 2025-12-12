"""
Application Factory Function

This function, create_app, serves as an application factory for Flask.
It creates and configures a Flask application, initializes necessary
extensions, registers blueprints for modular organization, and returns
the configured app.
"""
from flask import Flask

from app.core.config import Config
from app.core.extensions import db, jwt, migrate


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration settings from the provided config class.
    app.config.from_object(config_class)

    # Initialize Flask extensions: SQLAlchemy, Flask-Migrate,
    # and Flask-JWT-Extended.
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Import and register API blueprints
    from app.api import auth_bp, users_bp, projects_bp, tasks_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(tasks_bp, url_prefix="/api/project")

    return app
