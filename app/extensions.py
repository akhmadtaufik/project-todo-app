from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Initializing Flask-SQLAlchemy for database management.
db = SQLAlchemy()

# Initializing Flask-Migrate for handling database migrations.
migrate = Migrate()

# Initializing Flask-JWT-Extended for implementing
# JSON Web Token (JWT) based authentication.
jwt = JWTManager()
