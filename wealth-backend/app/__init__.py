from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from .config import DevelopmentConfig, ProductionConfig, TestingConfig
import os

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

def create_app(config_class=None):
    app = Flask(__name__)

    # Configure app based on the environment or passed config class
    env = os.environ.get('FLASK_ENV', 'development')
    if config_class:
        app.config.from_object(config_class)
    elif env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize extensions with the app
    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Import and register blueprints
    from .auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import routes_bp
    app.register_blueprint(routes_bp, url_prefix='/')

    return app
