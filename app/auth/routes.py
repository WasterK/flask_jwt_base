# auth/routes.py
from flask import Blueprint, request, jsonify
from .services import AuthService
from .schemas import AuthSchema

auth_bp = Blueprint('auth', __name__)
auth_schema = AuthSchema()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    errors = auth_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    result, status_code = AuthService.register_user(data['username'], data['password'])
    return jsonify(result), status_code


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = auth_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    token, status_code = AuthService.authenticate_user(data['username'], data['password'])
    if status_code == 200:
        return jsonify(token), status_code
    return jsonify({"message": "Invalid credentials"}), status_code

@auth_bp.route('/verify', methods=['POST'])
def verify():
    token = request.headers.get('Authorization').split()[1]
    username = AuthService.verify_token(token)
    if username:
        return jsonify({"username": username}), 200
    return jsonify({"message": "Token is invalid or expired"}), 401
