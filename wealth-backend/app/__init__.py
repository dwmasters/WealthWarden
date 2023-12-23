from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure your database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dwmasters:BMMDWMasters0341**@localhost:3306/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import blueprints
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # More configuration and initialization can go here...
    with app.app_context():
        db.create_all()

    return app
