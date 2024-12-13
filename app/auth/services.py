import hashlib
from flask_jwt_extended import create_access_token, decode_token
import datetime
from app.auth.models import UserModule

SECRET_KEY = '553aa87a5422643cd35c60d617ac6aafb4e1499c57fabeec78f285062fa1e634'

class AuthService:
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def register_user(data):
        db = UserModule()
        # Check if the user already exists
        existing_user = db.get_user_by_username(data["user_name"])
        if existing_user:
            db.close_connection()
            return {"message": "Username already exists. Please log in."}, 409

        # Proceed with registration
        password_hash = AuthService.hash_password(data["password_hash"])
        user_id = db.create_user(data["employee_id"], data["user_name"], data["email"], password_hash, data["first_name"], data["last_name"], data["mobile_number"], data["created_by"])
        db.close_connection()

        if user_id:
            return {"message": "User registered successfully", "user_id": user_id}, 201
        return {"message": "User registration failed."}, 500

    @staticmethod
    def authenticate_user(user_name, password):
        db = UserModule()
        user = db.get_user_by_username(user_name)
        if user:
            password_hash = AuthService.hash_password(password)
            if user[4] == password_hash:
                
                access_token = create_access_token(identity=str(user[0]), expires_delta=datetime.timedelta(minutes=1))
                db.close_connection()
                return {"token": access_token}, 200
            db.close_connection()
            return {"message": "Invalid password."}, 401
        db.close_connection()
        return {"message": "User not found. Please sign up."}, 401

    @staticmethod
    def verify_token(token):
        try:
            user_id = decode_token(token)
            return user_id
        except Exception as e:
            return None
