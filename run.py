"""
Flask Application Entry Point

Use this file to run the Flask application.
Debug mode is controlled by config, NOT hardcoded.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug mode is determined by app.config['DEBUG'], not hardcoded
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=app.config.get('DEBUG', False)
    )
