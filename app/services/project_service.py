"""
Project Service

Business logic for project operations.
"""
from typing import List, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError

from app.core.extensions import db
from app.models.project import Projects
from app.schemas.project import ProjectResponse, ProjectBasicResponse, ProjectWithTasks


class ProjectService:
    """Service class for project operations."""

    @staticmethod
    def get_user_projects(user_id: str, limit: int = 10) -> List[dict]:
        """
        Get all projects for a user with pagination.
        
        Returns:
            List of project dictionaries
        """
        projects = Projects.query.filter_by(user_id=user_id).limit(limit).all()
        return [ProjectWithTasks.from_orm_project(p).model_dump() for p in projects]

    @staticmethod
    def get_project_by_id(project_id: int) -> Optional[Projects]:
        """Get a project by ID."""
        return Projects.query.get(project_id)

    @staticmethod
    def check_project_permission(project_id: int, user_id: str) -> bool:
        """Check if user owns the project."""
        project = Projects.query.filter_by(id=project_id, user_id=user_id).first()
        return project is not None

    @staticmethod
    def create_project(project_name: str, description: str, user_id: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Create a new project.
        
        Returns:
            Tuple of (success, message, project_data)
        """
        if not project_name or not description or not user_id:
            return False, "Invalid parameters for creating a project.", None

        try:
            new_project = Projects(
                project_name=project_name,
                description=description,
                user_id=user_id
            )
            db.session.add(new_project)
            db.session.commit()
            return True, "Project successfully created", ProjectWithTasks.from_orm_project(new_project).model_dump()
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error creating project: {str(e)}", None

    @staticmethod
    def update_project(project: Projects, project_name: str, description: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Update a project.
        
        Returns:
            Tuple of (success, message, project_data)
        """
        if not project_name or not description:
            return False, "Incomplete data. Please provide all required fields.", None

        try:
            project.project_name = project_name
            project.description = description
            db.session.commit()
            return True, "Project successfully updated", ProjectBasicResponse.from_orm_project(project).model_dump()
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error updating project: {str(e)}", None

    @staticmethod
    def delete_project(project: Projects) -> Tuple[bool, str]:
        """
        Delete a project.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            db.session.delete(project)
            db.session.commit()
            return True, "Project successfully deleted"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error deleting project: {str(e)}"

    @staticmethod
    def serialize_project(project: Projects) -> dict:
        """Serialize project to dictionary format."""
        return ProjectWithTasks.from_orm_project(project).model_dump()

    @staticmethod
    def serialize_project_basic(project: Projects) -> dict:
        """Serialize project with basic fields only."""
        return ProjectBasicResponse.from_orm_project(project).model_dump()
