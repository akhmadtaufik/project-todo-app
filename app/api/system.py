"""
System API Routes

Health check and system status endpoints.
"""
import time
from flask import Blueprint, jsonify
from sqlalchemy import text

from app.core.extensions import db

system_bp = Blueprint("system", __name__)

# Track application start time
APP_START_TIME = time.time()


@system_bp.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        200: System healthy with database connection status and uptime
        503: System unhealthy
    """
    health_status = {
        "status": "healthy",
        "uptime_seconds": round(time.time() - APP_START_TIME, 2),
        "database": "disconnected",
    }
    
    # Check database connection
    try:
        db.session.execute(text("SELECT 1"))
        health_status["database"] = "connected"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["database"] = f"error: {str(e)}"
        return jsonify(health_status), 503
    
    return jsonify(health_status), 200


@system_bp.route("/ready", methods=["GET"])
def readiness_check():
    """
    Readiness check for Kubernetes/container orchestration.
    
    Returns:
        200: Application ready to serve traffic
        503: Application not ready
    """
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"ready": True}), 200
    except Exception:
        return jsonify({"ready": False}), 503
