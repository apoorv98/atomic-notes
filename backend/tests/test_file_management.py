#!/usr/bin/env python3

import pytest
from flask import Flask
from sqlalchemy.orm import Session
from app import create_app, db
from app.models.user import User
from app.models.note import Note
from app.services.file_service import create_note, get_note, update_note, delete_note
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def app():
    print("Creating app")
    app = create_app('testing')
    print(f"App created: {app}")
    print(f"App type: {type(app)}")
    assert isinstance(app, Flask), "app is not a Flask instance"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    print(f"Creating client for app: {app}")
    return app.test_client()

@pytest.fixture(scope='module')
def test_user(app):
    print(f"Creating test user for app: {app}")
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    return user_id

@pytest.fixture(scope='module')
def access_token(app, test_user):
    print(f"Creating access token for app: {app} and user id: {test_user}")
    with app.app_context():
        return create_access_token(identity=test_user)

@pytest.fixture(autouse=True)
def session(app):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        session = Session(bind=connection)

        # Patch the db.session to use our scoped session
        old_session = db.session
        db.session = session

        yield session

        db.session = old_session
        session.close()
        transaction.rollback()
        connection.close()

def test_create_note(client, test_user, access_token):
    print(f"Running test_create_note")
    response = client.post('/api/notes', json={
        'title': 'Test Note',
        'content': '# Test Note\n\nThis is a test note.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['title'] == 'Test Note'

def test_get_note(client, test_user, access_token):
    print(f"Running test_get_note")
    note = create_note(test_user, 'Test Note', '# Test Note\n\nThis is a test note.')
    response = client.get(f'/api/notes/{note.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['title'] == 'Test Note'
    assert response.json['content'] == '# Test Note\n\nThis is a test note.'

def test_update_note(client, test_user, access_token):
    print(f"Running test_update_note")
    note = create_note(test_user, 'Test Note', '# Test Note\n\nThis is a test note.')
    response = client.put(f'/api/notes/{note.id}', json={
        'title': 'Updated Note',
        'content': '# Updated Note\n\nThis note has been updated.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Note'
    assert response.json['content'] == '# Updated Note\n\nThis note has been updated.'

def test_delete_note(client, test_user, access_token):
    print(f"Running test_delete_note")
    note = create_note(test_user, 'Test Note', '# Test Note\n\nThis is a test note.')
    response = client.delete(f'/api/notes/{note.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204
    assert get_note(note.id) is None
