from flask import Flask
from flask_jwt_extended import JWTManager
from app.devices.routes import devices_bp
from app.auth.models import User  # Import User class from auth.models
from app.database.access import DatabaseAccess

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    jwt = JWTManager(app)

    # Create tables if they don't exist
    db_access = DatabaseAccess()
    User.create_table()  # Ensure User class is used correctly

    # Register Blueprints
    from app.auth.routes import auth_bp
    from app.devices.routes import devices_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(devices_bp, url_prefix='/devices')

    return app
