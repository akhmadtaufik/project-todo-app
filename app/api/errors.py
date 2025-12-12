"""
Global Error Handlers

Consistent JSON error responses with information hiding.
Internal details are logged, not exposed to clients.
"""
import structlog
from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError

errors_bp = Blueprint("errors", __name__)
logger = structlog.get_logger()


def create_error_response(code: int, message: str, details: list = None):
    """Create a standardized error response."""
    response = {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        response["error"]["details"] = details
    return jsonify(response), code


@errors_bp.app_errorhandler(400)
def bad_request(error):
    """Handle bad request errors."""
    return create_error_response(400, "Bad request")


@errors_bp.app_errorhandler(401)
def unauthorized(error):
    """Handle unauthorized errors."""
    return create_error_response(401, "Authentication required")


@errors_bp.app_errorhandler(403)
def forbidden(error):
    """Handle forbidden errors."""
    return create_error_response(403, "Access forbidden")


@errors_bp.app_errorhandler(404)
def not_found(error):
    """Handle not found errors - return JSON, not HTML."""
    return create_error_response(404, "Resource not found")


@errors_bp.app_errorhandler(405)
def method_not_allowed(error):
    """Handle method not allowed errors."""
    return create_error_response(405, "Method not allowed")


@errors_bp.app_errorhandler(422)
def unprocessable_entity(error):
    """Handle validation errors."""
    return create_error_response(422, "Validation error")


@errors_bp.app_errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit errors."""
    # Log the rate limit event
    logger.warning("rate_limit_exceeded", description=str(error))
    return create_error_response(429, "Too many requests. Please try again later.")


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    """
    Handle internal server errors.
    Log full details server-side, return generic message to client.
    """
    # Log the full error details for debugging
    logger.error(
        "internal_server_error",
        error=str(error),
        error_type=type(error).__name__
    )
    
    # Return generic message - DO NOT expose internal details
    return create_error_response(500, "Internal server error")


@errors_bp.app_errorhandler(Exception)
def handle_exception(error):
    """
    Handle all unhandled exceptions.
    Log full stack trace, return generic error to client.
    """
    # Log the full exception for debugging
    logger.exception(
        "unhandled_exception",
        error=str(error),
        error_type=type(error).__name__
    )
    
    # Pass through HTTP exceptions with their codes
    if isinstance(error, HTTPException):
        return create_error_response(error.code, error.description)
    
    # Handle Pydantic validation errors
    if isinstance(error, ValidationError):
        errors = []
        for err in error.errors():
            field = ".".join(str(loc) for loc in err["loc"])
            errors.append({"field": field, "message": err["msg"]})
        return create_error_response(422, "Validation error", errors)
    
    # Return generic 500 for all other exceptions - HIDE internal details
    return create_error_response(500, "An unexpected error occurred")
