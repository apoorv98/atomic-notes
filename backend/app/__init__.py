#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name):
    print(f"Creating app with config: {config_name}")
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    jwt.init_app(app)

    # Import blueprints
    from .routes.auth import auth as auth_blueprint
    from .routes.notes import notes as notes_blueprint

    # Register blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(notes_blueprint, url_prefix='/api/notes')

    print(f"App created: {app}")
    return app
