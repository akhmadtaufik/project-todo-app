"""
Global Error Handlers

Consistent JSON error responses for all HTTP errors.
"""
from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

errors_bp = Blueprint("errors", __name__)


def create_error_response(code: int, message: str):
    """Create a standardized error response."""
    return jsonify({
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }), code


@errors_bp.app_errorhandler(400)
def bad_request(error):
    """Handle bad request errors."""
    message = getattr(error, 'description', 'Bad request')
    return create_error_response(400, message)


@errors_bp.app_errorhandler(401)
def unauthorized(error):
    """Handle unauthorized errors."""
    message = getattr(error, 'description', 'Authentication required')
    return create_error_response(401, message)


@errors_bp.app_errorhandler(403)
def forbidden(error):
    """Handle forbidden errors."""
    message = getattr(error, 'description', 'Access forbidden')
    return create_error_response(403, message)


@errors_bp.app_errorhandler(404)
def not_found(error):
    """Handle not found errors."""
    message = getattr(error, 'description', 'Resource not found')
    return create_error_response(404, message)


@errors_bp.app_errorhandler(422)
def unprocessable_entity(error):
    """Handle validation errors."""
    message = getattr(error, 'description', 'Validation error')
    return create_error_response(422, message)


@errors_bp.app_errorhandler(429)
def rate_limit_exceeded(error):
    """Handle rate limit errors."""
    message = getattr(error, 'description', 'Rate limit exceeded. Please try again later.')
    return create_error_response(429, message)


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    """Handle internal server errors."""
    # Log the actual error for debugging
    import structlog
    logger = structlog.get_logger()
    logger.error("internal_server_error", error=str(error))
    
    return create_error_response(500, 'An internal server error occurred')


@errors_bp.app_errorhandler(Exception)
def handle_exception(error):
    """Handle all unhandled exceptions."""
    import structlog
    logger = structlog.get_logger()
    logger.exception("unhandled_exception", error=str(error))
    
    # Pass through HTTP exceptions
    if isinstance(error, HTTPException):
        return create_error_response(error.code, error.description)
    
    # Return generic 500 for non-HTTP exceptions
    return create_error_response(500, 'An unexpected error occurred')
