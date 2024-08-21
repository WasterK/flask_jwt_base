import hashlib
from flask_jwt_extended import create_access_token
import datetime
from app.auth.models import User

SECRET_KEY = '553aa87a5422643cd35c60d617ac6aafb4e1499c57fabeec78f285062fa1e634'

class AuthService:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(username, password):
        # Check if the user already exists
        existing_user = User.find_by_username(username)
        if existing_user:
            return {"message": "Username already exists. Please log in."}, 409

        # Proceed with registration if the user does not exist
        password_hash = AuthService.hash_password(password)
        User.insert(username, password_hash)
        return {"message": "User registered successfully"}, 201

    @staticmethod
    def authenticate_user(username, password):
        user = User.find_by_username(username)
        if user:
            # Check if the provided password matches the stored hash
            if user.check_password(password):
                # Create a JWT token that expires in 24 hours
                access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(minutes=1))
                return {"token": access_token}, 200
            else:
                return {"message": "Invalid password."}, 401
        else:
            return {"message": "User not found. Please sign up."}, 401
