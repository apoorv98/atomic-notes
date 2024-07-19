#!/usr/bin/env python3

import pytest
from app import create_app
from app.models.user import User
from app.models.note import Note
from app.services.file_service import create_note, get_note, update_note, delete_note
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

@pytest.fixture
def user():
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    return user

@pytest.fixture
def access_token(user):
    return create_access_token(identity=user.id)

def test_create_note(client, user, access_token):
    response = client.post('/api/notes', json={
        'title': 'Test Note',
        'content': '# Test Note\n\nThis is a test note.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['title'] == 'Test Note'

def test_get_note(client, user, access_token):
    note = create_note(user.id, 'Test Note', '# Test Note\n\nThis is a test note.')
    response = client.get(f'/api/notes/{note.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['title'] == 'Test Note'
    assert response.json['content'] == '# Test Note\n\nThis is a test note.'

def test_update_note(client, user, access_token):
    note = create_note(user.id, 'Test Note', '# Test Note\n\nThis is a test note.')
    response = client.put(f'/api/notes/{note.id}', json={
        'title': 'Updated Note',
        'content': '# Updated Note\n\nThis note has been updated.'
    }, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
    assert response.json['title'] == 'Updated Note'
    assert response.json['content'] == '# Updated Note\n\nThis note has been updated.'

def test_delete_note(client, user, access_token):
    note = create_note(user.id, 'Test Note', '# Test Note\n\nThis is a test note.')
    response = client.delete(f'/api/notes/{note.id}', headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 204
    assert get_note(note.id) is None
