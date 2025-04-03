# app/__init__.py
from flask import Flask

def create_app(config_object=None):
    """
    Application factory function that creates and configures the Flask app
    """
    app = Flask(__name__)
    
    # Configure the app
    if config_object:
        app.config.from_object(config_object)
    else:
        # Default configuration
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    return app