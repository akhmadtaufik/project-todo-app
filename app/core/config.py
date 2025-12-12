"""
Application Configuration

Loads configuration from environment variables.
All credentials MUST be set in .env - no fallback values.
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


def get_required_env(key: str) -> str:
    """Get required environment variable or raise error."""
    value = os.environ.get(key)
    if not value:
        raise ValueError(f"Required environment variable '{key}' is not set")
    return value


class Config:
    """Base configuration class - requires all env vars to be set."""
    
    # Secret keys (REQUIRED)
    SECRET_KEY = get_required_env('SECRET_KEY')
    JWT_SECRET_KEY = get_required_env('JWT_SECRET_KEY')
    
    # Database configuration (REQUIRED)
    SQLALCHEMY_DATABASE_URI = get_required_env('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
