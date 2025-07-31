from unittest import result
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash

from app.services.auth_services import register_user, validate_user

auth_api = Blueprint('auth_api', __name__, url_prefix='/api/auth')

@auth_api.route('/register', methods=['POST'])
def api_register():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    result = register_user(username, email, password)
    return jsonify(result), result.get("status_code", 200)
    

@auth_api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    result = validate_user(username, password)

    if result["success"]:
        user_data = result["data"]
        access_token = create_access_token(identity=str(user_data["id"]))
        refresh_token = create_refresh_token(identity=str(user_data["id"]))
        result["access_token"] = access_token
        result["refresh_token"] = refresh_token
    return jsonify(result), result.get("status_code", 200)
    pass