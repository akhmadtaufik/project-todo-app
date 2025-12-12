"""
Application Factory Function

This function, create_app, serves as an application factory for Flask.
It creates and configures a Flask application, initializes necessary
extensions, registers blueprints for modular organization, and returns
the configured app.
"""
import os
from flask import Flask

from app.core.config import get_config
from app.core.extensions import db, jwt, migrate, limiter, talisman
from app.core.logger import setup_logging, RequestLoggingMiddleware


def create_app(config_class=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration based on environment if not specified
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    # Setup structured logging
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    log_file = app.config.get('LOG_FILE', 'app.log')
    setup_logging(log_level, log_file)

    # Initialize Flask extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    
    # Initialize Talisman (security headers) with dev-friendly settings
    # In production, use stricter CSP and force HTTPS
    is_development = app.config.get('DEBUG', False)
    talisman.init_app(
        app,
        force_https=not is_development,
        strict_transport_security=not is_development,
        content_security_policy=None if is_development else {
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline'",
            'style-src': "'self' 'unsafe-inline'",
            'img-src': "'self' data:",
        },
    )
    
    # Initialize Swagger/OpenAPI documentation
    from flasgger import Swagger
    swagger_template = app.config.get('SWAGGER_TEMPLATE', {})
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        "openapi": "3.0.0"
    }
    Swagger(app, template=swagger_template, config=swagger_config)
    
    # Import and initialize security callbacks (JWT token revocation, etc.)
    with app.app_context():
        from app.core import security  # noqa: F401 - registers JWT callbacks
    
    # Import and register API blueprints
    from app.api import auth_bp, users_bp, projects_bp, tasks_bp, system_bp, errors_bp
    
    # Register error handlers first (app-wide)
    app.register_blueprint(errors_bp)
    
    # Register API blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(system_bp)  # /health and /ready at root
    
    # Add request logging middleware
    if not is_development:
        app.wsgi_app = RequestLoggingMiddleware(app.wsgi_app)

    return app
