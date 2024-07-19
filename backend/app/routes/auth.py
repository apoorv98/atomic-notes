#!/usr/bin/env python3

from flask import Blueprint, request, jsonify
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
