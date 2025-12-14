"""
API Module

Registers all API blueprints.
"""
from flask import Blueprint
from flask_cors import CORS

# Create blueprints
auth_bp = Blueprint("auth", __name__)
users_bp = Blueprint("users", __name__)
projects_bp = Blueprint("projects", __name__)
tasks_bp = Blueprint("tasks", __name__)

# Enable CORS for all blueprints with explicit configuration
cors_config = {
    "origins": ["http://localhost:3000"],  # Frontend URL
    "supports_credentials": True,  # Allow cookies/auth headers
    "allow_headers": ["Content-Type", "Authorization"],
    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
}

CORS(auth_bp, **cors_config)
CORS(users_bp, **cors_config)
CORS(projects_bp, **cors_config)
CORS(tasks_bp, **cors_config)

# Import routes after blueprint creation to avoid circular imports
from app.api import auth, users, projects, tasks

# Import system and error blueprints
from app.api.system import system_bp
from app.api.errors import errors_bp
