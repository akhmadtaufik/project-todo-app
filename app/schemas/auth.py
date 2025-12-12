"""
Authentication Schemas

Pydantic models for Auth request/response validation.
"""
from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Schema for login request."""
    email: str
    password: str


class RegisterRequest(BaseModel):
    """Schema for registration request."""
    name: str
    email: str
    password: str


class TokenResponse(BaseModel):
    """Schema for token response."""
    message: str
    access_token: str
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Schema for refresh token response."""
    access_token: str
