"""
Task Service

Business logic for task operations.
"""
from datetime import datetime, date
from typing import List, Optional, Tuple
from sqlalchemy.exc import SQLAlchemyError

from app.core.extensions import db
from app.models.task import Tasks
from app.models.project import Projects
from app.schemas.task import TaskResponse, TaskBasicResponse


class TaskService:
    """Service class for task operations."""

    @staticmethod
    def has_permission(project_id: int, user_id: str) -> bool:
        """Check if user has permission to access a project's tasks."""
        project = Projects.query.filter_by(id=project_id, user_id=user_id).first()
        return project is not None

    @staticmethod
    def is_valid_project(project_id: int, user_id: str) -> bool:
        """Check if a project exists and belongs to the user."""
        project = Projects.query.filter_by(id=project_id, user_id=user_id).first()
        return project is not None

    @staticmethod
    def validate_due_date(due_date_str: str) -> Tuple[bool, str, Optional[date]]:
        """
        Validate due date is in correct format and not in the past.
        
        Returns:
            Tuple of (is_valid, message, parsed_date)
        """
        try:
            current_date = datetime.now().date()
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            
            if due_date < current_date:
                return False, "Due date must be later than the current date", None
                
            return True, "", due_date
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD", None

    @staticmethod
    def get_tasks_by_project(project_id: int) -> List[dict]:
        """
        Get all tasks for a project.
        
        Returns:
            List of task dictionaries
        """
        tasks = db.session.execute(
            db.select(Tasks)
            .join(Projects, Tasks.project_id == Projects.id)
            .filter(Tasks.project_id == project_id)
            .order_by(Tasks.id)
        ).scalars()
        
        return [TaskResponse.from_orm_task(task).model_dump() for task in tasks]

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Tasks]:
        """Get a task by ID."""
        return Tasks.query.filter_by(id=task_id).first()

    @staticmethod
    def get_task_by_id_and_project(task_id: int, project_id: int) -> Optional[Tasks]:
        """Get a task by ID and project ID."""
        return Tasks.query.filter_by(id=task_id, project_id=project_id).first()

    @staticmethod
    def create_task(
        task_name: str,
        description: str,
        due_date: date,
        status: str,
        project_id: int
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Create a new task.
        
        Returns:
            Tuple of (success, message, task_data)
        """
        try:
            new_task = Tasks(
                task_name=task_name,
                description=description,
                due_date=due_date,
                status=status,
                project_id=project_id
            )
            db.session.add(new_task)
            db.session.commit()
            return True, "Task successfully created", TaskResponse.from_orm_task(new_task).model_dump()
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error creating task: {str(e)}", None

    @staticmethod
    def update_task(
        task: Tasks,
        task_name: str,
        description: str,
        due_date: str,
        status: str,
        project_id: int
    ) -> Tuple[bool, str, Optional[dict]]:
        """
        Update a task.
        
        Returns:
            Tuple of (success, message, task_data)
        """
        try:
            task.task_name = task_name
            task.description = description
            task.due_date = due_date
            task.status = status
            task.project_id = project_id
            db.session.commit()
            return True, "Task successfully updated", TaskBasicResponse.from_orm_task(task).model_dump()
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error updating task: {str(e)}", None

    @staticmethod
    def delete_task(task: Tasks) -> Tuple[bool, str]:
        """
        Delete a task.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            db.session.delete(task)
            db.session.commit()
            return True, "Task successfully deleted"
        except SQLAlchemyError as e:
            db.session.rollback()
            return False, f"Error deleting task: {str(e)}"

    @staticmethod
    def serialize_task(task: Tasks) -> dict:
        """Serialize task to dictionary format."""
        return TaskResponse.from_orm_task(task).model_dump()

    @staticmethod
    def serialize_task_basic(task: Tasks) -> dict:
        """Serialize task with basic fields only."""
        return TaskBasicResponse.from_orm_task(task).model_dump()
