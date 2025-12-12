"""
Flask Extensions

Centralized initialization of Flask extensions.
"""
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

# Initializing Flask-SQLAlchemy for database management.
db = SQLAlchemy()

# Initializing Flask-Migrate for handling database migrations.
migrate = Migrate()

# Initializing Flask-JWT-Extended for implementing
# JSON Web Token (JWT) based authentication.
jwt = JWTManager()

# Initializing Flask-Limiter for rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Initializing Flask-Talisman for security headers
# Note: CSP and HTTPS forcing disabled for development
talisman = Talisman()

# Note: Swagger (flasgger) is initialized directly in the app factory
# with the template configuration, not as a shared extension.


