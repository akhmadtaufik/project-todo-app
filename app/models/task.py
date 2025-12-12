from app.core.extensions import db


class Tasks(db.Model):
    """Task model for individual work items."""
    __tablename__ = "tasks"
    
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DATE)
    status = db.Column(db.String(50))
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    update_at = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now()
    )

    def __repr__(self):
        return f"<Task {self.task_name}>"

