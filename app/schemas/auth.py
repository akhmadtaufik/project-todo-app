"""
Authentication Schemas

Pydantic models with strict validation for security.
"""
import re
import bleach
from pydantic import BaseModel, EmailStr, Field, field_validator


# Security patterns to block
SQL_INJECTION_PATTERN = re.compile(
    r"(--|;|'|\"|\bOR\b|\bAND\b|\bUNION\b|\bSELECT\b|\bDROP\b|\bINSERT\b|\bDELETE\b|\bUPDATE\b)",
    re.IGNORECASE
)


def sanitize_string(value: str, max_length: int = 255) -> str:
    """Sanitize string input - strip, limit length, remove HTML."""
    if not value:
        return value
    # Strip whitespace
    value = value.strip()
    # Remove HTML tags
    value = bleach.clean(value, tags=[], strip=True)
    # Limit length
    return value[:max_length]


def check_sql_injection(value: str, field_name: str) -> str:
    """Check for potential SQL injection patterns."""
    if SQL_INJECTION_PATTERN.search(value):
        raise ValueError(f"{field_name} contains invalid characters")
    return value


class LoginRequest(BaseModel):
    """Schema for login request with strict validation."""
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=1, max_length=128)
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Sanitize and validate email."""
        return sanitize_string(v.lower(), 255)


class RegisterRequest(BaseModel):
    """Schema for registration request with security validation."""
    name: str = Field(..., min_length=2, max_length=100, description="User's display name")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, max_length=128, description="Secure password")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Sanitize and validate name."""
        v = sanitize_string(v, 100)
        if len(v) < 2:
            raise ValueError("Name must be at least 2 characters")
        check_sql_injection(v, "name")
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Sanitize and validate email."""
        return sanitize_string(v.lower(), 255)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r'[A-Za-z]', v):
            raise ValueError("Password must contain at least one letter")
        if not re.search(r'\d', v):
            raise ValueError("Password must contain at least one number")
        return v


class TokenResponse(BaseModel):
    """Schema for token response."""
    success: bool = True
    message: str
    access_token: str
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Schema for refresh token response."""
    success: bool = True
    access_token: str
