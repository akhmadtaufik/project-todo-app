"""
Token Blocklist Model

Stores revoked JWT tokens for logout functionality.
"""
from datetime import datetime
from app.core.extensions import db


class TokenBlocklist(db.Model):
    """Model to store revoked JWT tokens."""
    __tablename__ = "token_blocklist"
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True, index=True)
    token_type = db.Column(db.String(10), nullable=False)  # 'access' or 'refresh'
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f"<TokenBlocklist {self.jti}>"
    
    @classmethod
    def is_token_revoked(cls, jti: str) -> bool:
        """Check if a token is in the blocklist."""
        return cls.query.filter_by(jti=jti).first() is not None
    
    @classmethod
    def add_token(cls, jti: str, token_type: str, user_id: int = None, expires_at: datetime = None):
        """Add a token to the blocklist."""
        token = cls(
            jti=jti,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at
        )
        db.session.add(token)
        db.session.commit()
        return token
