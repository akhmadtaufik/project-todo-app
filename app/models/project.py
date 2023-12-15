from app.extensions import db


class Projects(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    update_at = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now()
    )

    tasks = db.relationship("Task", backref="projects", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "project_name": self.project_name,
            "description": self.description,
            "user_id": self.user_id,
            "created_at": str(self.created_at),
            "update_at": str(self.created_at),
            "task": [task.serialize() for task in self.tasks],  # type: ignore
        }
