"""
Application Configuration

Strict environment validation using pydantic-settings.
Application WILL CRASH at startup if critical vars are missing or weak.
"""
import os
from datetime import timedelta
from typing import Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Strict settings validation - crashes app if critical vars are missing/weak.
    All values loaded from environment variables.
    """
    
    # Critical Required Settings (crash if missing or weak)
    DATABASE_URL: str = Field(..., min_length=10)
    SECRET_KEY: str = Field(..., min_length=32)
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    
    # Optional Settings with defaults
    FLASK_ENV: str = Field(default="development")
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE: str = Field(default="app.log")
    REDIS_URL: Optional[str] = Field(default="memory://")
    
    @field_validator('SECRET_KEY', 'JWT_SECRET_KEY')
    @classmethod
    def validate_secret_strength(cls, v: str, info) -> str:
        """Ensure secrets are not default/weak values."""
        weak_patterns = ['secret', 'password', '123456', 'default', 'change']
        if len(v) < 32:
            raise ValueError(f"{info.field_name} must be at least 32 characters")
        # Check for weak patterns (case-insensitive)
        v_lower = v.lower()
        for pattern in weak_patterns:
            if pattern in v_lower and len(v) < 50:
                raise ValueError(f"{info.field_name} appears weak - use a stronger secret")
        return v
    
    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith(('postgresql://', 'postgres://', 'sqlite://')):
            raise ValueError("DATABASE_URL must be a valid PostgreSQL or SQLite URL")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Allow extra env vars not defined in Settings


# Load and validate settings at module load time
# This will CRASH the app if validation fails
settings = Settings()


class FlaskConfig:
    """Base Flask configuration class - uses validated settings."""
    
    # Secret keys (validated by pydantic-settings)
    SECRET_KEY = settings.SECRET_KEY
    JWT_SECRET_KEY = settings.JWT_SECRET_KEY
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = settings.DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_COOKIE_SECURE = True  # Only send JWT cookies over HTTPS
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = settings.REDIS_URL
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Session Security (Anti-CSRF, XSS, Session Hijacking)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging
    LOG_LEVEL = settings.LOG_LEVEL
    LOG_FILE = settings.LOG_FILE
    
    # Swagger/OpenAPI Configuration
    SWAGGER_TEMPLATE = {
        "openapi": "3.0.0",
        "info": {
            "title": "Todo API",
            "version": "1.0.0",
            "description": "A RESTful API for managing todo projects and tasks with JWT authentication"
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Enter your JWT access token"
                }
            }
        },
        "security": [{"BearerAuth": []}]
    }


class DevelopmentConfig(FlaskConfig):
    """Development configuration - relaxed security for local dev."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    JWT_COOKIE_SECURE = False
    LOG_LEVEL = 'DEBUG'


class TestingConfig(FlaskConfig):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    JWT_COOKIE_SECURE = False


class ProductionConfig(FlaskConfig):
    """Production configuration - maximum security, DEBUG ALWAYS FALSE."""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'WARNING'
    # All security settings remain True from base class


# Config selector based on FLASK_ENV
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get config class based on FLASK_ENV."""
    env = settings.FLASK_ENV
    return config_by_name.get(env, DevelopmentConfig)
