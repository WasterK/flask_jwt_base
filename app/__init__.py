from flask import Flask
from flask_jwt_extended import JWTManager
from app.auth.models import UserModule  # Import User class from auth.models

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    jwt = JWTManager(app)

    # Register Blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
