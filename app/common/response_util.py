"""
Response Utilities

Standardized API response formatting.
"""
from flask import jsonify
from typing import Any, Optional, Tuple


def generate_response(
    success: bool,
    message: str,
    data: Optional[Any] = None,
    status_code: int = 200
) -> Tuple[Any, int]:
    """
    Generate a standardized JSON response.
    
    Args:
        success: Whether the operation was successful
        message: Human-readable message
        data: Optional response data
        status_code: HTTP status code
        
    Returns:
        Tuple of (JSON response, status code)
    """
    response_data = {"success": success, "message": message}
    if data is not None:
        response_data["data"] = data
    return jsonify(response_data), status_code


def error_response(message: str, status_code: int = 400) -> Tuple[Any, int]:
    """Generate an error response."""
    return generate_response(False, message, status_code=status_code)


def success_response(
    message: str,
    data: Optional[Any] = None,
    status_code: int = 200
) -> Tuple[Any, int]:
    """Generate a success response."""
    return generate_response(True, message, data=data, status_code=status_code)
