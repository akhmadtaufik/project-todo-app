"""
Structured Logging Configuration

JSON-formatted logs for production observability.
Logs to both console and file.
"""
import sys
import logging
import structlog
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str = "app.log"):
    """
    Configure structured logging with console and file handlers.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file
    """
    # Ensure log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )
    
    # Add file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    logging.getLogger().addHandler(file_handler)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger()


def get_logger():
    """Get the configured structlog logger."""
    return structlog.get_logger()


class RequestLoggingMiddleware:
    """WSGI middleware to log requests and responses."""
    
    def __init__(self, app):
        self.app = app
        self.logger = structlog.get_logger()
    
    def __call__(self, environ, start_response):
        # Log request
        path = environ.get('PATH_INFO', '')
        method = environ.get('REQUEST_METHOD', '')
        
        self.logger.info(
            "request_started",
            method=method,
            path=path,
            remote_addr=environ.get('REMOTE_ADDR', ''),
        )
        
        # Capture response status
        response_status = [None]
        
        def custom_start_response(status, response_headers, exc_info=None):
            response_status[0] = status
            return start_response(status, response_headers, exc_info)
        
        try:
            response = self.app(environ, custom_start_response)
            self.logger.info(
                "request_completed",
                method=method,
                path=path,
                status=response_status[0],
            )
            return response
        except Exception as e:
            self.logger.exception(
                "request_failed",
                method=method,
                path=path,
                error=str(e),
            )
            raise
