"""
Projects API Tests

Tests for project CRUD endpoints.
"""
import pytest
from tests.conftest import create_test_user, get_auth_headers


class TestCreateProject:
    """Tests for POST /api/projects/ endpoint."""
    
    def test_create_project_success(self, client, auth_headers):
        """Test successful project creation."""
        response = client.post(
            "/api/projects/",
            json={
                "project_name": "My Test Project",
                "description": "A project for testing"
            },
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data["success"] is True
        assert "data" in data
        assert data["data"]["project_name"] == "My Test Project"
    
    def test_create_project_without_auth(self, client):
        """Test project creation without authentication."""
        response = client.post(
            "/api/projects/",
            json={
                "project_name": "My Test Project",
                "description": "A project for testing"
            }
        )
        
        assert response.status_code == 401
    
    def test_create_project_missing_fields(self, client, auth_headers):
        """Test project creation with missing required fields."""
        response = client.post(
            "/api/projects/",
            json={
                "project_name": "My Test Project"
                # Missing description
            },
            headers=auth_headers
        )
        
        assert response.status_code == 422


class TestGetProjects:
    """Tests for GET /api/projects/ endpoint."""
    
    def test_get_projects_empty(self, client, auth_headers):
        """Test getting projects when user has none."""
        response = client.get("/api/projects/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_get_projects_with_data(self, client, auth_headers):
        """Test getting projects after creating some."""
        # Create projects
        for i in range(3):
            client.post(
                "/api/projects/",
                json={
                    "project_name": f"Project {i}",
                    "description": f"Description {i}"
                },
                headers=auth_headers
            )
        
        # Get projects
        response = client.get("/api/projects/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert len(data["data"]) == 3
        assert "meta" in data
        assert data["meta"]["total_items"] == 3
    
    def test_get_projects_without_auth(self, client):
        """Test getting projects without authentication."""
        response = client.get("/api/projects/")
        
        assert response.status_code == 401


class TestProjectIsolation:
    """Tests to ensure users can only access their own projects."""
    
    def test_users_see_only_own_projects(self, client):
        """Test that users can only see their own projects."""
        # Create first user and their project
        create_test_user(client, "User One", "user1@example.com", "Password123")
        headers1 = get_auth_headers(client, "user1@example.com", "Password123")
        
        client.post(
            "/api/projects/",
            json={
                "project_name": "User 1 Project",
                "description": "Belongs to user 1"
            },
            headers=headers1
        )
        
        # Create second user and their project
        create_test_user(client, "User Two", "user2@example.com", "Password456")
        headers2 = get_auth_headers(client, "user2@example.com", "Password456")
        
        client.post(
            "/api/projects/",
            json={
                "project_name": "User 2 Project",
                "description": "Belongs to user 2"
            },
            headers=headers2
        )
        
        # User 1 should only see their project
        response1 = client.get("/api/projects/", headers=headers1)
        data1 = response1.get_json()
        assert len(data1["data"]) == 1
        assert data1["data"][0]["project_name"] == "User 1 Project"
        
        # User 2 should only see their project
        response2 = client.get("/api/projects/", headers=headers2)
        data2 = response2.get_json()
        assert len(data2["data"]) == 1
        assert data2["data"][0]["project_name"] == "User 2 Project"


class TestGetProjectById:
    """Tests for GET /api/projects/{id} endpoint."""
    
    def test_get_project_by_id_success(self, client, auth_headers):
        """Test getting a specific project by ID."""
        # Create a project
        create_response = client.post(
            "/api/projects/",
            json={
                "project_name": "Test Project",
                "description": "Test description"
            },
            headers=auth_headers
        )
        project_id = create_response.get_json()["data"]["project_id"]
        
        # Get the project
        response = client.get(f"/api/projects/{project_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert data["data"]["project_name"] == "Test Project"
    
    def test_get_nonexistent_project(self, client, auth_headers):
        """Test getting a project that doesn't exist."""
        response = client.get("/api/projects/99999", headers=auth_headers)
        
        assert response.status_code == 404
