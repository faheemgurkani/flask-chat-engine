# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
    DEBUG = False
    TESTING = False
    FLASK_ENV = 'production'
    
    # Database settings
    DATABASE_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../data/final.db')

class DevelopmentConfig(Config):
    """Development config."""
    DEBUG = True
    FLASK_ENV = 'development'

class TestingConfig(Config):
    """Testing config."""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Production config."""
    # Production specific settings
    pass