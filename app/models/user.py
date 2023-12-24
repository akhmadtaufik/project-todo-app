from app.extensions import db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(1024), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    update_at = db.Column(
        db.TIMESTAMP, server_default=db.func.now(), onupdate=db.func.now()
    )

    projects = db.relationship(
        "Projects", backref="users", cascade="all, delete-orphan"
    )

    def serialize(self):
        return {
            "user_id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": str(self.created_at),
            "update_at": str(self.update_at),
            "project_list": [project.serialize() for project in self.projects],  # type: ignore
        }

    def basic_serialize(self):
        return {
            "username": self.name,
            "email": self.email,
            "update_at": str(self.update_at),
        }
