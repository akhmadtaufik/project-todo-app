from app.core.extensions import db


class Projects(db.Model):
    """Project model for organizing tasks."""
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

    tasks = db.relationship("Tasks", backref="projects", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project {self.project_name}>"

