"""
Authentication API Tests

Tests for user registration and login endpoints.
"""
import pytest


class TestRegistration:
    """Tests for POST /api/auth/register endpoint."""
    
    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post("/api/auth/register", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123"
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert "message" in data
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields."""
        response = client.post("/api/auth/register", json={
            "email": "john@example.com"
            # Missing name and password
        })
        
        assert response.status_code == 422
        data = response.get_json()
        assert data["success"] is False
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post("/api/auth/register", json={
            "name": "John Doe",
            "email": "invalid-email",
            "password": "SecurePass123"
        })
        
        assert response.status_code == 422
        data = response.get_json()
        assert data["success"] is False
    
    def test_register_weak_password(self, client):
        """Test registration with weak password (too short)."""
        response = client.post("/api/auth/register", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "weak"  # Less than 8 characters
        })
        
        assert response.status_code == 422
        data = response.get_json()
        assert data["success"] is False
    
    def test_register_duplicate_email(self, client):
        """Test registration with already registered email."""
        # Register first user
        client.post("/api/auth/register", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123"
        })
        
        # Try to register with same email
        response = client.post("/api/auth/register", json={
            "name": "Jane Doe",
            "email": "john@example.com",  # Same email
            "password": "AnotherPass123"
        })
        
        assert response.status_code == 422
        data = response.get_json()
        assert data["success"] is False


class TestLogin:
    """Tests for POST /api/auth/login endpoint."""
    
    def test_login_success(self, client):
        """Test successful login returns access token."""
        # Register user first
        client.post("/api/auth/register", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123"
        })
        
        # Login
        response = client.post("/api/auth/login", json={
            "email": "john@example.com",
            "password": "SecurePass123"
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "access_token" in data
        assert "refresh_token" in data
        assert len(data["access_token"]) > 0
    
    def test_login_invalid_email(self, client):
        """Test login with non-existent email."""
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "SomePassword123"
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
    
    def test_login_wrong_password(self, client):
        """Test login with wrong password."""
        # Register user
        client.post("/api/auth/register", json={
            "name": "John Doe",
            "email": "john@example.com",
            "password": "SecurePass123"
        })
        
        # Login with wrong password
        response = client.post("/api/auth/login", json={
            "email": "john@example.com",
            "password": "WrongPassword123"
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False
    
    def test_login_missing_password(self, client):
        """Test login with missing password field."""
        response = client.post("/api/auth/login", json={
            "email": "john@example.com"
        })
        
        assert response.status_code == 422
        data = response.get_json()
        assert data["success"] is False
