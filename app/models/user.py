from app.core.extensions import db


class Users(db.Model):
    """User model for authentication and profile data."""
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

    def __repr__(self):
        return f"<User {self.email}>"

