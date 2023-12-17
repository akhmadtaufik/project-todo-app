from app.extensions import db


class Tasks(db.Model):
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

    def serialize(self):
        return {
            "task_id": self.id,
            "task_name": self.task_name,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "project_id": self.project_id,
            "created_at": str(self.created_at),
            "update_at": str(self.update_at),
        }

    def basic_serialize(self):
        return {
            "task_name": self.task_name,
            "description": self.description,
            "due_date": self.due_date,
            "status": self.status,
            "update_at": str(self.update_at),
        }
