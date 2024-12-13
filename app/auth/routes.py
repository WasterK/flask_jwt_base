from flask import Blueprint, request, jsonify
from .services import AuthService
from .schemas import SignupSchema, AuthSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)
auth_schema = AuthSchema()
signup_schema = SignupSchema()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    errors = signup_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    result, status_code = AuthService.register_user(data)
    return jsonify(result), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = auth_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    result, status_code = AuthService.authenticate_user(data['user_name'], data['password_hash'])
    return jsonify(result), status_code

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()  
def profile():
    current_user = get_jwt_identity() 
    return jsonify(logged_in_as=current_user), 200