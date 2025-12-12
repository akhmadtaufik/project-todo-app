"""
Test Configuration and Fixtures

Provides pytest fixtures for testing the Flask application.
"""
import pytest
from typing import Dict, Generator

from app import create_app
from app.core.extensions import db
from app.models.user import Users
from app.models.project import Projects
from app.models.task import Tasks


class TestingConfig:
    """Testing configuration with in-memory SQLite database."""
    TESTING = True
    DEBUG = True
    
    # Use in-memory SQLite for fast, isolated tests
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    SECRET_KEY = "test-secret-key-for-testing-only-32chars!"
    JWT_SECRET_KEY = "test-jwt-secret-key-for-testing-32chars!"
    JWT_ACCESS_TOKEN_EXPIRES = False  # Tokens don't expire in tests
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Security settings relaxed for testing
    SESSION_COOKIE_SECURE = False
    JWT_COOKIE_SECURE = False
    
    # Rate limiting disabled for tests
    RATELIMIT_ENABLED = False


@pytest.fixture
def app() -> Generator:
    """
    Create and configure a test application instance.
    
    Uses in-memory SQLite for fast, isolated tests.
    Creates all tables before each test and drops them after.
    """
    test_app = create_app(TestingConfig)
    
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """
    Create a test client for making HTTP requests.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a test CLI runner.
    """
    return app.test_cli_runner()


def create_test_user(client, name: str = "Test User", email: str = "test@example.com", 
                     password: str = "SecurePass123") -> Dict:
    """
    Helper function to register a test user.
    
    Returns:
        Response JSON from registration
    """
    response = client.post("/api/auth/register", json={
        "name": name,
        "email": email,
        "password": password
    })
    return response.get_json()


def get_auth_token(client, email: str = "test@example.com", 
                   password: str = "SecurePass123") -> str:
    """
    Helper function to get JWT access token.
    
    Returns:
        JWT access token string
    """
    response = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    data = response.get_json()
    return data.get("access_token", "")


def get_auth_headers(client, email: str = "test@example.com", 
                     password: str = "SecurePass123") -> Dict[str, str]:
    """
    Helper function to get Authorization headers with JWT token.
    
    Returns:
        Dictionary with Authorization header
    """
    token = get_auth_token(client, email, password)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def auth_headers(client) -> Dict[str, str]:
    """
    Fixture that creates a test user and returns auth headers.
    
    Use this fixture for tests that need authenticated access.
    """
    # Register the test user
    create_test_user(client)
    # Return headers with token
    return get_auth_headers(client)


@pytest.fixture
def second_user_headers(client) -> Dict[str, str]:
    """
    Fixture that creates a second test user for isolation testing.
    """
    create_test_user(
        client, 
        name="Second User", 
        email="second@example.com", 
        password="SecondPass123"
    )
    return get_auth_headers(client, "second@example.com", "SecondPass123")
