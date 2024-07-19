#!/usr/bin/env python3

from app.models.user import User, db
from flask_jwt_extended import create_access_token
import re

def register_user(username, email, password):
    if User.query.filter_by(username=username).first():
        return {'error': 'Username already exists'}, 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {'error': 'Invalid email format'}, 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return {'user_id': new_user.id}, 201

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return {'token': access_token}, 200
    return {'error': 'Invalid username or password'}, 401
