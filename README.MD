# RESTful API Documentation - Project Todo App

## 1. Project Overview

### Introduction

This document provides detailed information about the RESTful API for the Project Todo App. This API allows users to manage projects and tasks, including user registration, authentication, and CRUD operations for projects and their associated tasks.

### Purpose of the API

The primary purpose of this API is to serve as the backend for a to-do list application where users can organize their work into projects and manage individual tasks within those projects.

### Technologies Used

- **Backend Framework:** Flask (Python)
- **Database:** SQLAlchemy (used with a relational database like PostgreSQL, MySQL, or SQLite)
- **Database Migrations:** Flask-Migrate (using Alembic)
- **Authentication:** JSON Web Tokens (JWT) via Flask-JWT-Extended
- **Web Server:** Werkzeug (Flask's default development server)
- **Language:** Python

## 2. Installation Guide

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- A relational database (e.g., PostgreSQL, MySQL, SQLite)

### Environment Setup

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd project-todo-app
    ```

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Configure Environment Variables:**
    Create a `.env` file in the root directory and add the necessary environment variables (see section 8). Minimally, you'll need `DATABASE_URL` and `JWT_SECRET_KEY`.
    Example for SQLite:

    ```env
    DATABASE_URL="sqlite:///./app.db"
    JWT_SECRET_KEY="your-super-secret-jwt-key"
    # Add other Flask configurations as needed, e.g.
    # FLASK_APP=run.py (or your entry point)
    # FLASK_DEBUG=1
    ```

    Example for PostgreSQL:

    ```env
    DATABASE_URL="postgresql://user:password@host:port/database_name"
    JWT_SECRET_KEY="your-super-secret-jwt-key"
    ```

### How to install dependencies

```bash
pip install -r requirements.txt
```

### How to run the development server

1. **Initialize the database and apply migrations:**
    Ensure your `FLASK_APP` environment variable is set (e.g., `export FLASK_APP=app:create_app` or `set FLASK_APP=app:create_app` on Windows). If you have a `config.py` that `create_app` uses, make sure it's configured.

    ```bash
    flask db init  # Only if running for the first time and no migrations folder exists
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

2. **Run the Flask development server:**
    If you have a `run.py` file at the root of your project like this:

    ```python
    # run.py
    from app import create_app
    from dotenv import load_dotenv

    load_dotenv() # To load .env variables

    app = create_app()

    if __name__ == "__main__":
        app.run(debug=True) # Debug should be False in production
    ```

    Then run:

    ```bash
    python run.py
    ```

    Or, using the Flask CLI directly (ensure `FLASK_APP` is set):

    ```bash
    flask run
    ```

    The API will typically be available at `http://127.0.0.1:5000`.

## 3. Authentication & Authorization

### Authentication Method Used

The API uses JSON Web Tokens (JWT) for authentication. Clients must include an `access_token` in the `Authorization` header for protected endpoints.

**Header Format:** `Authorization: Bearer <access_token>`

### How to get an Access Token

1. **Register a new user:** Send a `POST` request to `/api/auth/register` with user details (name, email, password).
2. **Login:** Send a `POST` request to `/api/auth/login` with the registered email and password. The response will include an `access_token` and a `refresh_token`.

### Authorization Rules

- **Public Endpoints:**
  - `POST /api/auth/register`: User registration.
  - `POST /api/auth/login`: User login.
- **Protected Endpoints (require a valid JWT access token in the `Authorization` header):**
  - `POST /api/auth/refresh`: Requires a valid JWT refresh token in the `Authorization` header.
  - `GET /api/users/`: Retrieves all users. *(Currently unprotected, consider adding admin role protection).*
  - `GET /api/users/<user_id>`: Retrieves a specific user. *(Currently unprotected, consider adding admin/owner protection).*
  - `PUT /api/users/<user_id>`: Updates a specific user. *(Currently unprotected, consider adding admin/owner protection).*
  - `DELETE /api/users/<user_id>`: Deletes a specific user. *(Currently unprotected, consider adding admin/owner protection).*
  - `GET /api/projects/`: Retrieves projects for the authenticated user.
  - `POST /api/projects/`: Creates a new project for the authenticated user.
  - `GET /api/projects/<project_id>`: Retrieves a specific project (must belong to the authenticated user).
  - `PUT /api/projects/<project_id>`: Updates a specific project (must belong to the authenticated user).
  - `DELETE /api/projects/<project_id>`: Deletes a specific project (must belong to the authenticated user).
  - `GET /api/project/<project_id>/tasks`: Retrieves tasks for a specific project (project must belong to the authenticated user).
  - `POST /api/project/task`: Creates a new task (project_id in body must belong to the authenticated user).
  - `PUT /api/project/<project_id>/task/<task_id>`: Updates a specific task (project must belong to the authenticated user).
  - `DELETE /api/project/<project_id>/task/<task_id>`: Deletes a specific task (project must belong to the authenticated user).

## 4. API Endpoints

Endpoints are grouped by resource. All protected endpoints require `Authorization: Bearer <access_token>` in headers, unless specified otherwise (e.g. for refresh token).

---

### Auth Resource (`/api/auth`)

#### 1. Register User

- **Endpoint:** `POST /api/auth/register`
- **Description:** Registers a new user.
- **Required Headers:** None
- **Request Body Schema:**

    ```json
    {
        "name": "string (required)",
        "email": "string (required, unique)",
        "password": "string (required)"
    }
    ```

- **Example Request:**

    ```bash
    curl -X POST http://localhost:5000/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123"
    }'
    ```

- **Response (Success 201):**

    ```json
    {
        "message": "Registration user is completed"
    }
    ```

- **Possible Status Codes:**
  - `201 Created`: User registered successfully.
  - `422 Unprocessable Entity`: Incomplete data (e.g., missing fields).
  - (Implicit) `409 Conflict` (returned as JSON message): Email already registered. (Actual code might be 200 with error message based on `app/auth/routes.py`)

#### 2. Login User

- **Endpoint:** `POST /api/auth/login`
- **Description:** Logs in an existing user and returns access and refresh tokens.
- **Required Headers:** None
- **Request Body Schema:**

    ```json
    {
        "email": "string (required)",
        "password": "string (required)"
    }
    ```

- **Example Request:**

    ```bash
    curl -X POST http://localhost:5000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "john.doe@example.com",
        "password": "securepassword123"
    }'
    ```

- **Response (Success 200):**

    ```json
    {
        "message": "Login successfully",
        "access_token": "string (JWT)",
        "refresh_token": "string (JWT)"
    }
    ```

- **Possible Status Codes:**
  - `200 OK`: Login successful.
  - `400 Bad Request`: Incomplete data or user not found.
  - `401 Unauthorized`: Invalid credentials.

#### 3. Refresh Access Token

- **Endpoint:** `POST /api/auth/refresh`
- **Description:** Generates a new access token using a valid refresh token.
- **Required Headers:**
  - `Authorization: Bearer <refresh_token>` (Note: Send the refresh token here)
- **Request Body Schema:** None
- **Example Request:**

    ```bash
    curl -X POST http://localhost:5000/api/auth/refresh \
    -H "Authorization: Bearer your_refresh_token_here"
    ```

- **Response (Success 200):**

    ```json
    {
        "access_token": "string (JWT)"
    }
    ```

- **Possible Status Codes:**
  - `200 OK`: Token refreshed successfully.
  - `401 Unauthorized`: Invalid or expired refresh token.

---

### Users Resource (`/api/users`)

#### Security Note: These endpoints are currently not JWT protected in the provided code. For a production API, these should be protected, likely requiring admin privileges or specific user ownership for PUT/DELETE operations

#### 1. Get All Users

- **Endpoint:** `GET /api/users/`
- **Description:** Retrieves a list of users.
- **Required Headers:** *(None currently, should be `Authorization: Bearer <access_token>` for admin)*
- **Query Parameters:**
  - `limit` (integer, optional, default: 10): Number of users to retrieve.
- **Example Request:**

    ```bash
    curl -X GET "http://localhost:5000/api/users/?limit=5"
    ```

- **Response (Success 200):**

    ```json
    {
        "success": true,
        "data": [
            {
                "user_id": 1,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "created_at": "YYYY-MM-DD HH:MM:SS",
                "update_at": "YYYY-MM-DD HH:MM:SS",
                "project_list": [
                    {
                        "project_id": 1,
                        "project_name": "Personal Project",
                        "description": "My personal tasks",
                        "user_id": 1,
                        "created_at": "YYYY-MM-DD HH:MM:SS",
                        "update_at": "YYYY-MM-DD HH:MM:SS",
                        "task": []
                    }
                ]
            }
            // ... more users
        ]
    }
    ```

- **Possible Status Codes:**
  - `200 OK`: Users retrieved successfully.
  - `422 Unprocessable Entity`: Invalid `limit` parameter.
  - `500 Internal Server Error`: Database error.

#### 2. Get User by ID

- **Endpoint:** `GET /api/users/<int:user_id>`
- **Description:** Retrieves a specific user by their ID.
- **Required Headers:** *(None currently, should be `Authorization: Bearer <access_token>` for admin or self)*
- **Path Parameters:**
  - `user_id` (integer, required): The ID of the user to retrieve.
- **Example Request:**

    ```bash
    curl -X GET http://localhost:5000/api/users/1
    ```

- **Response (Success 200):**

    ```json
    {
        "success": true,
        "data": {
            "user_id": 1,
            "name": "John Doe",
            "email": "john.doe@example.com",
            "created_at": "YYYY-MM-DD HH:MM:SS",
            "update_at": "YYYY-MM-DD HH:MM:SS",
            "project_list": [] // Simplified, actual might include projects
        }
    }
    ```

- **Possible Status Codes:**
  - `200 OK`: User retrieved successfully.
  - `404 Not Found`: User with the specified ID does not exist.
  - `500 Internal Server Error`: Database error.

#### 3. Update User

- **Endpoint:** `PUT /api/users/<int:user_id>`
- **Description:** Updates a specific user's details.
- **Required Headers:** *(None currently, should be `Authorization: Bearer <access_token>` for admin or self)*
- **Path Parameters:**
  - `user_id` (integer, required): The ID of the user to update.
- **Request Body Schema:**

    ```json
    {
        "username": "string (required)", // Note: model uses 'name', route uses 'username'
        "email": "string (required)",
        "password": "string (required)" // Note: password will be re-hashed
    }
    ```

- **Example Request:**

    ```bash
    curl -X PUT http://localhost:5000/api/users/1 \
    -H "Content-Type: application/json" \
    -d '{
        "username": "Johnathan Doe",
        "email": "john.doe.new@example.com",
        "password": "newsecurepassword123"
    }'
    ```

- **Response (Success 200):**

    ```json
    {
        "success": true,
        "message": "Data successfully updated",
        "data": {
            "username": "Johnathan Doe", // Corresponds to 'name' in model
            "email": "john.doe.new@example.com",
            "update_at": "YYYY-MM-DD HH:MM:SS"
        }
    }
    ```

- **Possible Status Codes:**
  - `200 OK`: User updated successfully.
  - `404 Not Found`: User with the specified ID does not exist.
  - `422 Unprocessable Entity`: Incomplete data.
  - `500 Internal Server Error`: Database error.

#### 4. Delete User

- **Endpoint:** `DELETE /api/users/<int:user_id>`
- **Description:** Deletes a specific user.
- **Required Headers:** *(None currently, should be `Authorization: Bearer <access_token>` for admin or self)*
- **Path Parameters:**
  - `user_id` (integer, required): The ID of the user to delete.
- **Example Request:**

    ```bash
    curl -X DELETE http://localhost:5000/api/users/1
    ```

- **Response (Success 204):**

    ```json
    {
        "success": true,
        "message": "User successfully deleted"
    }
    ```

    *(Note: A 204 response typically has no body, but the code returns a JSON message)*
- **Possible Status Codes:**
  - `204 No Content` (as per code, but returns body): User deleted successfully.
  - `404 Not Found`: User with the specified ID does not exist.
  - `500 Internal Server Error`: Error deleting user.

---

### Projects Resource (`/api/projects`)

All endpoints in this section require `Authorization: Bearer <access_token>` in headers.

#### 1. Get All Projects for Authenticated User

- **Endpoint:** `GET /api/projects/`
- **Description:** Retrieves all projects belonging to the authenticated user.
- **Query Parameters:**
  - `limit` (integer, optional, default: 10): Number of projects to retrieve.
- **Example Request:**

    ```bash
    curl -X GET "http://localhost:5000/api/projects/?limit=5" \
    -H "Authorization: Bearer your_access_token"
    ```

- **Response (Success 200):**

    ```json
    {
        "success": true,
        "message": "Projects retrieved successfully",
        "data": [
            {
                "project_id": 1,
                "project_name": "Work Project",
                "description": "Tasks related to work",
                "user_id": 123, // Authenticated user's ID
                "created_at": "YYYY-MM-DD HH:MM:SS",
                "update_at": "YYYY-MM-DD HH:MM:SS",
                "task": [
                    // ... list of task objects (serialized)
                ]
            }
            // ... more projects
        ]
    }
    ```

- **Possible Status Codes:**
  - `200 OK`: Projects retrieved successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `500 Internal Server Error`: Database error.

#### 2. Create New Project

- **Endpoint:** `POST /api/projects/`
- **Description:** Creates a new project for the authenticated user.
- **Request Body Schema:**

    ```json
    {
        "project_name": "string (required)",
        "description": "string (required)"
    }
    ```

- **Example Request:**

    ```bash
    curl -X POST http://localhost:5000/api/projects/ \
    -H "Authorization: Bearer your_access_token" \
    -H "Content-Type: application/json" \
    -d '{
        "project_name": "Home Renovation",
        "description": "Planning and tasks for renovating the house"
    }'
    ```

- **Response (Success 201):**

    ```json
    {
        "success": true,
        "message": "Project successfully created",
        "data": { // Serialized new project
            "project_id": 2,
            "project_name": "Home Renovation",
            "description": "Planning and tasks for renovating the house",
            "user_id": 123,
            "created_at": "YYYY-MM-DD HH:MM:SS",
            "update_at": "YYYY-MM-DD HH:MM:SS",
            "task": []
        }
    }
    ```

- **Possible Status Codes:**
  - `201 Created`: Project created successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `422 Unprocessable Entity`: Invalid parameters.
  - `500 Internal Server Error`: Database error.

#### 3. Get Project by ID

- **Endpoint:** `GET /api/projects/<int:id>`
- **Description:** Retrieves a specific project by its ID. The project must belong to the authenticated user.
- **Path Parameters:**
  - `id` (integer, required): The ID of the project to retrieve.
- **Example Request:**

    ```bash
    curl -X GET http://localhost:5000/api/projects/1 \
    -H "Authorization: Bearer your_access_token"
    ```

- **Response (Success 200):**

    ```json
    {
        "success": true,
        "message": "Project retrieved successfully",
        "data": { // Serialized project
            "project_id": 1,
            "project_name": "Work Project",
            // ... other fields
        }
    }
    ```

- **Possible Status Codes:**
  - `200 OK`: Project retrieved successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `404 Not Found`: Project not found or does not belong to the user.
  - `500 Internal Server Error`: Database error.

#### 4. Update Project

- **Endpoint:** `PUT /api/projects/<int:id>`
- **Description:** Updates a specific project. The project must belong to the authenticated user.
- **Path Parameters:**
  - `id` (integer, required): The ID of the project to update.
- **Request Body Schema:**

    ```json
    {
        "project_name": "string (required)",
        "description": "string (required)"
    }
    ```

- **Example Request:**

    ```bash
    curl -X PUT http://localhost:5000/api/projects/1 \
    -H "Authorization: Bearer your_access_token" \
    -H "Content-Type: application/json" \
    -d '{
        "project_name": "Updated Project Name",
        "description": "Updated description"
    }'
    ```

- **Response (Success 201 - Note: typically 200 for update):**

    ```json
    {
        "success": true,
        "message": "Project successfully updated",
        "data": { // Basic serialized project
            "project_name": "Updated Project Name",
            "description": "Updated description",
            "update_at": "YYYY-MM-DD HH:MM:SS"
        }
    }
    ```

- **Possible Status Codes:**
  - `201 Created` (as per code, usually `200 OK` for updates): Project updated successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `403 Forbidden`: User does not have permission to edit this project.
  - `404 Not Found`: Project not found.
  - `422 Unprocessable Entity`: Incomplete data.
  - `500 Internal Server Error`: Database error.

#### 5. Delete Project

- **Endpoint:** `DELETE /api/projects/<int:id>`
- **Description:** Deletes a specific project. The project must belong to the authenticated user.
- **Path Parameters:**
  - `id` (integer, required): The ID of the project to delete.
- **Example Request:**

    ```bash
    curl -X DELETE http://localhost:5000/api/projects/1 \
    -H "Authorization: Bearer your_access_token"
    ```

- **Response (Success 204 - Note: code returns body):**

    ```json
    {
        "success": true,
        "message": "Project successfully deleted"
    }
    ```

- **Possible Status Codes:**
  - `204 No Content` (as per code, but returns body): Project deleted successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `403 Forbidden`: User does not have permission to delete this project.
  - `404 Not Found`: Project not found.
  - `500 Internal Server Error`: Database error.

---

### Tasks Resource (`/api/project`)

All endpoints in this section require `Authorization: Bearer <access_token>` in headers.

#### 1. Get All Tasks for a Project

- **Endpoint:** `GET /api/project/<int:project_id>/tasks`
- **Description:** Retrieves all tasks for a specific project. The project must belong to the authenticated user.
- **Path Parameters:**
  - `project_id` (integer, required): The ID of the project whose tasks are to be retrieved.
- **Example Request:**

    ```bash
    curl -X GET http://localhost:5000/api/project/1/tasks \
    -H "Authorization: Bearer your_access_token"
    ```

- **Response (Success 200):**

    ```json
    {
        "success": true,
        "message": "Tasks retrieved successfully",
        "data": [
            {
                "task_id": 1,
                "task_name": "Design homepage",
                "description": "Create mockups for the new homepage",
                "due_date": "YYYY-MM-DD",
                "status": "Pending",
                "project_id": 1,
                "created_at": "YYYY-MM-DD HH:MM:SS",
                "update_at": "YYYY-MM-DD HH:MM:SS"
            }
            // ... more tasks
        ]
    }
    ```

- **Possible Status Codes:**
  - `200 OK`: Tasks retrieved successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `403 Forbidden`: User does not have permission for this project or project ID is invalid.
  - `500 Internal Server Error`: Database error.

#### 2. Create New Task

- **Endpoint:** `POST /api/project/task` (Note: `project_id` is in the body, not path)
- **Description:** Creates a new task within a specified project. The project must belong to the authenticated user.
- **Request Body Schema:**

    ```json
    {
        "task_name": "string (required)",
        "description": "string (required)",
        "due_date": "string (required, YYYY-MM-DD format, must not be in the past)",
        "status": "string (required)",
        "project_id": "integer (required, must be a valid project ID of the user)"
    }
    ```

- **Example Request:**

    ```bash
    curl -X POST http://localhost:5000/api/project/task \
    -H "Authorization: Bearer your_access_token" \
    -H "Content-Type: application/json" \
    -d '{
        "task_name": "Implement login feature",
        "description": "Develop the user login functionality",
        "due_date": "2025-12-31",
        "status": "In Progress",
        "project_id": 1
    }'
    ```

- **Response (Success 201):**

    ```json
    {
        "success": true,
        "message": "Task successfully created",
        "data": { // Serialized new task
            "task_id": 2,
            "task_name": "Implement login feature",
            // ... other fields
            "project_id": 1
        }
    }
    ```

- **Possible Status Codes:**
  - `201 Created`: Task created successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `403 Forbidden`: User does not have permission or invalid `project_id`.
  - `422 Unprocessable Entity`: Invalid parameters (e.g., missing fields, past due date).
  - `500 Internal Server Error`: Database error.

#### 3. Update Task

- **Endpoint:** `PUT /api/project/<int:project_id>/task/<int:task_id>`
- **Description:** Updates a specific task. The project must belong to the authenticated user.
- **Path Parameters:**
  - `project_id` (integer, required): The ID of the project containing the task.
  - `task_id` (integer, required): The ID of the task to update.
- **Request Body Schema:**

    ```json
    {
        "task_name": "string (required)",
        "description": "string (required)",
        "due_date": "string (required, YYYY-MM-DD format)", // Past date check not mentioned for update in code
        "status": "string (required)"
    }
    ```

- **Example Request:**

    ```bash
    curl -X PUT http://localhost:5000/api/project/1/task/2 \
    -H "Authorization: Bearer your_access_token" \
    -H "Content-Type: application/json" \
    -d '{
        "task_name": "Implement login feature (updated)",
        "description": "Develop and test the user login functionality",
        "due_date": "2026-01-15",
        "status": "Completed"
    }'
    ```

- **Response (Success 201 - Note: typically 200 for update):**

    ```json
    {
        "success": true,
        "message": "Task successfully updated",
        "data": { // Basic serialized task
            "task_name": "Implement login feature (updated)",
            "description": "Develop and test the user login functionality",
            "due_date": "2026-01-15",
            "status": "Completed",
            "update_at": "YYYY-MM-DD HH:MM:SS"
        }
    }
    ```

- **Possible Status Codes:**
  - `201 Created` (as per code, usually `200 OK` for updates): Task updated successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `403 Forbidden`: User does not have permission or invalid `project_id`.
  - `404 Not Found`: Task not found.
  - `422 Unprocessable Entity`: Incomplete data.
  - `500 Internal Server Error`: Database error.

#### 4. Delete Task

- **Endpoint:** `DELETE /api/project/<int:project_id>/task/<int:task_id>`
- **Description:** Deletes a specific task. The project must belong to the authenticated user.
- **Path Parameters:**
  - `project_id` (integer, required): The ID of the project containing the task.
  - `task_id` (integer, required): The ID of the task to delete.
- **Example Request:**

    ```bash
    curl -X DELETE http://localhost:5000/api/project/1/task/2 \
    -H "Authorization: Bearer your_access_token"
    ```

- **Response (Success 204 - Note: code returns body):**

    ```json
    {
        "success": true,
        "message": "Task successfully deleted"
    }
    ```

- **Possible Status Codes:**
  - `204 No Content` (as per code, but returns body): Task deleted successfully.
  - `401 Unauthorized`: Invalid or missing token.
  - `403 Forbidden`: User does not have permission or invalid `project_id`.
  - `404 Not Found`: Task not found.
  - `500 Internal Server Error`: Database error.

---

## 5. Data Models

### User (`Users`)

| Field       | Type         | Constraints                     | Description                     |
|-------------|--------------|---------------------------------|---------------------------------|
| `id`        | Integer      | Primary Key                     | Unique identifier for the user  |
| `name`      | String(64)   | Not Nullable                    | Name of the user                |
| `email`     | String(128)  | Not Nullable, Unique            | Email address of the user       |
| `password`  | String(1024) | Not Nullable                    | Hashed password of the user     |
| `created_at`| TIMESTAMP    | Server Default (current time)   | Timestamp of user creation      |
| `update_at` | TIMESTAMP    | Server Default, On Update       | Timestamp of last user update   |
| `projects`  | Relationship | `Projects` (backref `users`)    | Projects associated with user   |

**Serialized Output (`user.serialize()`):**

```json
{
    "user_id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "created_at": "YYYY-MM-DD HH:MM:SS.ffffff",
    "update_at": "YYYY-MM-DD HH:MM:SS.ffffff",
    "project_list": [ /* array of serialized project objects */ ]
}
```

**Basic Serialized Output (`user.basic_serialize()`):**

```json
{
    "username": "John Doe", // Note: key is 'username', value from 'name'
    "email": "john.doe@example.com",
    "update_at": "YYYY-MM-DD HH:MM:SS.ffffff"
}
```

### Project (`Projects`)

| Field          | Type         | Constraints                               | Description                         |
|----------------|--------------|-------------------------------------------|-------------------------------------|
| `id`           | Integer      | Primary Key                               | Unique identifier for the project   |
| `project_name` | String(128)  | Not Nullable                              | Name of the project                 |
| `description`  | Text         |                                           | Description of the project          |
| `user_id`      | Integer      | Foreign Key (`users.id`), Not Nullable, On Delete CASCADE | ID of the user owning the project |
| `created_at`   | TIMESTAMP    | Server Default (current time)             | Timestamp of project creation       |
| `update_at`    | TIMESTAMP    | Server Default, On Update                 | Timestamp of last project update    |
| `tasks`        | Relationship | `Tasks` (backref `projects`)              | Tasks associated with the project   |

**Serialized Output (`project.serialize()`):**

```json
{
    "project_id": 1,
    "project_name": "My Project",
    "description": "Project description",
    "user_id": 1,
    "created_at": "YYYY-MM-DD HH:MM:SS.ffffff",
    "update_at": "YYYY-MM-DD HH:MM:SS.ffffff", // Note: model uses self.created_at for update_at in serialize
    "task": [ /* array of serialized task objects */ ]
}
```

**Basic Serialized Output (`project.basic_serialize()`):**

```json
{
    "project_name": "My Project",
    "description": "Project description",
    "update_at": "YYYY-MM-DD HH:MM:SS.ffffff" // Note: model uses self.created_at for update_at in basic_serialize
}
```

*(Note on Project serialization: `update_at` in serialized output seems to mistakenly use `self.created_at`. This should be `self.update_at`)*

### Task (`Tasks`)

| Field       | Type         | Constraints                               | Description                       |
|-------------|--------------|-------------------------------------------|-----------------------------------|
| `id`        | Integer      | Primary Key                               | Unique identifier for the task    |
| `task_name` | String(128)  | Not Nullable                              | Name of the task                  |
| `description`| Text         |                                           | Description of the task           |
| `due_date`  | DATE         |                                           | Due date of the task              |
| `status`    | String(50)   |                                           | Current status of the task        |
| `project_id`| Integer      | Foreign Key (`projects.id`), Not Nullable, On Delete CASCADE | ID of the project this task belongs to |
| `created_at`| TIMESTAMP    | Server Default (current time)             | Timestamp of task creation        |
| `update_at` | TIMESTAMP    | Server Default, On Update                 | Timestamp of last task update     |

**Serialized Output (`task.serialize()`):**

```json
{
    "task_id": 1,
    "task_name": "My Task",
    "description": "Task description",
    "due_date": "YYYY-MM-DD", // Date object, will be stringified
    "status": "Pending",
    "project_id": 1,
    "created_at": "YYYY-MM-DD HH:MM:SS.ffffff",
    "update_at": "YYYY-MM-DD HH:MM:SS.ffffff"
}
```

**Basic Serialized Output (`task.basic_serialize()`):**

```json
{
    "task_name": "My Task",
    "description": "Task description",
    "due_date": "YYYY-MM-DD",
    "status": "Pending",
    "update_at": "YYYY-MM-DD HH:MM:SS.ffffff"
}
```

## 6. Error Handling

### Standard Error Response Format

Most error responses follow this format:

```json
{
    "success": false, // Usually for custom handled errors
    "message": "A descriptive error message"
}
```

Flask-JWT-Extended errors might have a different structure, e.g., `{"msg": "Error message"}`.
Standard Flask error handlers (like 404 Not Found) might return HTML or a simpler JSON if not customized.

### Common Error Messages and Meanings

- **Authentication (`/api/auth`)**
  - `"Incomplete data. Please provide all required fields."` (422 or 400): Missing name, email, or password during registration or login.
  - `"Email '<email>' is already registered."` (Implicit 409, actual code might vary): Attempting to register with an email that already exists.
  - `"User not found"` (400): Email provided during login does not correspond to any user.
  - `"Invalid credentials. Check your password."` (401): Password provided during login is incorrect.
  - JWT specific errors (e.g., `Token has expired`, `Invalid token`) from Flask-JWT-Extended (usually 401 or 422).
- **Users (`/api/users`)**
  - `"Invalid parameter"` (422): `limit` query parameter is not a valid integer.
  - `"User not found"` (404): The specified `user_id` does not exist.
  - `"Database error"` (500): A generic error occurred during database operation.
  - `"Data not complete"` (422): Missing required fields during user update.
  - `"Error deleting user"` (500): An error occurred during user deletion.
- **Projects (`/api/projects`)**
  - `"Error retrieving projects: <error_details>"` (500): Generic database error.
  - `"Invalid parameters for creating a project."` (422): Missing `project_name` or `description`.
  - `"Error creating project: <error_details>"` (500): Generic database error.
  - `"Project not found. Please verify the project ID exists."` (404): Project ID does not exist.
  - `"You do not have permission to edit this project"` (403): Authenticated user is not the owner of the project.
  - `"Incomplete data. Please provide all required fields."` (422): Missing fields during project update.
  - `"Error updating project: <error_details>"` (500): Generic database error.
  - `"Error deleting project: <error_details>"` (500): Generic database error.
- **Tasks (`/api/project/.../tasks`)**
  - `"You do not have permission to retrieve these tasks/create tasks/update tasks/delete tasks"` (403): Authenticated user does not own the parent project.
  - `"Task not found. Please verify the project ID"` (403): Project ID is invalid or doesn't belong to the user (used in `get_all_task_by_project_id`).
  - `"Error retrieving tasks: <error_details>"` (500): Generic database error.
  - `"Invalid project_id for creating a task/updating a task/deleting a task"` (403): The `project_id` provided in request body or path does not belong to the authenticated user.
  - `"Invalid parameters for creating a task"` (422): Missing required fields for task creation.
  - `"Due date must be later than the current date"` (422): `due_date` for new task is in the past.
  - `"Error creating task: <error_details>"` (500): Generic database error.
  - `"Task not found"` (404): The specified `task_id` does not exist.
  - `"Data not complete"` (422): Missing fields during task update.
  - `"Error updating task: <error_details>"` (500): Generic database error.
  - `"Error deleting task: <error_details>"` (500): Generic database error.

## 7. Testing Guide

*(This section is speculative as no test files or configurations were provided in the file listing.)*

### How to run the tests

Typically, tests would be run using a test runner like `pytest` or Python's built-in `unittest` module.
If `pytest` is used:

```bash
pytest
```

Or for `unittest`:

```bash
python -m unittest discover tests
```

(Assuming tests are in a `tests` directory)

### Tools used for testing

- **Test Runner:** Likely `pytest` or `unittest`.
- **Test Client:** Flask provides a test client (`app.test_client()`) for making requests to the application without running a live server.
- **Assertions:** Standard Python `assert` statements or specific assertion methods from the testing framework.
- **Database Management:** Tests might involve setting up a separate test database or using in-memory SQLite, and managing its state (creation, teardown, fixtures).
- **Mocking:** Libraries like `unittest.mock` might be used to mock external dependencies or parts of the application.

### Structure of the test files

A common structure would be a `tests/` directory at the root of the project:

```plaintext
project-todo-app/
├── app/
├── tests/
│   ├── __init__.py
│   ├── conftest.py  # (for pytest fixtures)
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_projects.py
│   ├── test_tasks.py
│   └── ... (other test files or utility modules)
└── ... (other project files)
```

Each `test_*.py` file would contain test cases for the corresponding application module or resource.

## 8. Environment Variables

The application is configured using environment variables, typically loaded from a `.env` file in the root directory using a library like `python-dotenv` (not listed in `requirements.txt` but common).

| Variable         | Description                                     | Example Value (SQLite)          | Example Value (PostgreSQL)                     | Required |
|------------------|-------------------------------------------------|---------------------------------|------------------------------------------------|----------|
| `FLASK_APP`      | Specifies the Flask application entry point.    | `app:create_app` or `run.py`    | `app:create_app` or `run.py`                   | Yes (for Flask CLI) |
| `FLASK_DEBUG`    | Enables/disables Flask debug mode.              | `1` (True) or `0` (False)       | `1` (True) or `0` (False)                      | No (defaults to False) |
| `DATABASE_URL`   | Connection string for the SQLAlchemy database.  | `sqlite:///./app.db`            | `postgresql://user:pass@host:port/dbname`      | Yes      |
| `JWT_SECRET_KEY` | Secret key for signing JWTs.                    | `your-very-secret-key`          | `another-super-secure-key`                   | Yes      |
| `SQLALCHEMY_TRACK_MODIFICATIONS` | SQLAlchemy event system toggle. | `False` (recommended)           | `False` (recommended)                          | No (defaults, but good to set) |
| `SQLALCHEMY_ECHO`| Logs SQL queries to console if True.          | `True` (for debugging)          | `True` (for debugging)                         | No       |

#### Note: The exact list of environment variables depends on the `config.py` file, which was not inspected. The above are common for Flask-SQLAlchemy and Flask-JWT-Extended

## 9. Deployment

*(This section is a general guide as specific deployment configurations were not provided.)*

### Guide for deploying to production

1. **Choose a Hosting Platform:** Options include Heroku, AWS (EC2, Elastic Beanstalk), Google Cloud (App Engine, Compute Engine), Azure App Service, DigitalOcean, etc.
2. **Production Web Server:** Do NOT use the Flask development server (`flask run` or `app.run(debug=True)`) in production. Use a production-grade WSGI server like Gunicorn or uWSGI.
    Example with Gunicorn:

    ```bash
    pip install gunicorn
    gunicorn --workers 4 --bind 0.0.0.0:8000 run:app # Assuming run.py creates 'app'
    ```

3. **Database Setup:**
    - Use a robust, managed database service (e.g., Amazon RDS, Google Cloud SQL, Heroku Postgres).
    - Ensure the `DATABASE_URL` environment variable points to the production database.
4. **Environment Variables:**
    - Set all required environment variables (see section 8) on the production server.
    - **CRITICAL:** `FLASK_DEBUG` must be `0` (False) in production.
    - `JWT_SECRET_KEY` must be a strong, unique, and secret string.
5. **Static Files:** If your Flask app serves static files (though this API seems primarily backend), configure your web server (like Nginx or Apache) or a CDN to serve them efficiently.
6. **Apply Migrations:** Run `flask db upgrade` in the production environment after deploying new code that includes database schema changes.
7. **Dependencies:** Ensure `requirements.txt` is up-to-date and install them in the production environment.
8. **Logging and Monitoring:** Set up proper logging (e.g., to files or a logging service) and monitoring tools to track application health and performance.
9. **HTTPS:** Ensure your application is served over HTTPS. Hosting platforms often provide this, or you can configure it with a reverse proxy like Nginx using Let's Encrypt certificates.

### Environment Configuration Tips

- **Separate Configurations:** Use different configuration classes or files for development, testing, and production (e.g., `config.py` with `DevelopmentConfig`, `ProductionConfig`). The `create_app` factory can then load the appropriate config based on an environment variable like `FLASK_ENV`.
- **Secrets Management:** Store sensitive information like `DATABASE_URL` and `JWT_SECRET_KEY` securely (e.g., using platform-specific secret stores, HashiCorp Vault) and not directly in version control.
- **`.gitignore`:** Ensure `.env` files, `instance` folders (if used for SQLite), and `__pycache__` directories are in `.gitignore`.

