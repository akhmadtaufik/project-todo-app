"""
Flask Application Entry Point

Use this file to run the Flask application.
Database migrations are handled by Flask-Migrate (flask db migrate/upgrade).
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
