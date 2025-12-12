"""
Application Configuration

Loads configuration from environment variables.
All credentials MUST be set in .env - no fallback values.
Supports Development, Testing, and Production environments.
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


def get_env(key: str, default: str = None) -> str:
    """Get optional environment variable with default."""
    return os.environ.get(key, default)


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
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = get_env('REDIS_URL', 'memory://')
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    RATELIMIT_HEADERS_ENABLED = True
    
    # Security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging
    LOG_LEVEL = get_env('LOG_LEVEL', 'INFO')
    LOG_FILE = get_env('LOG_FILE', 'app.log')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = get_env('TEST_DATABASE_URL', Config.SQLALCHEMY_DATABASE_URI)


class ProductionConfig(Config):
    """Production configuration - DEBUG is always False."""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'WARNING'


# Config selector based on FLASK_ENV
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get config class based on FLASK_ENV."""
    env = get_env('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
