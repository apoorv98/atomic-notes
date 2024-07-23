#!/usr/bin/env python3

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.services.auth_service import register_user, login_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result, status_code = register_user(data.get('username'), data.get('email'), data.get('password'))
    return jsonify(result), status_code

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result, status_code = login_user(data.get('username'), data.get('password'))
    return jsonify(result), status_code

@auth.route('/verify', methods=['GET'])
@jwt_required
def verify_token():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify({
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200
