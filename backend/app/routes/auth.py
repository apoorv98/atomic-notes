#!/usr/bin/env python3

from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result, status_code = register_user(data['username'], data['email'], data['password'])
    return jsonify(result), status_code

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result, status_code = login_user(data['username'], data['password'])
    return jsonify(result), status_code
