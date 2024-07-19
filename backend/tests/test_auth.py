#!/usr/bin/env python3

import pytest
from app import create_app
from app.models.user import User
from app.services.auth_service import register_user

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_user_registration(client):
    # Test user registration with valid data
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'securepassword123'
    })
    assert response.status_code == 201
    assert 'user_id' in response.json

    # Test user registration with existing username
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'another@example.com',
        'password': 'anotherpassword123'
    })
    assert response.status_code == 400
    assert 'error' in response.json

    # Test user registration with invalid email
    response = client.post('/api/auth/register', json={
        'username': 'newuser',
        'email': 'invalid-email',
        'password': 'validpassword123'
    })
    assert response.status_code == 400
    assert 'error' in response.json

def test_user_login(client):
    # Register a user first
    register_user('logintest', 'login@example.com', 'loginpassword123')

    # Test successful login
    response = client.post('/api/auth/login', json={
        'username': 'logintest',
        'password': 'loginpassword123'
    })
    assert response.status_code == 200
    assert 'token' in response.json

    # Test login with incorrect password
    response = client.post('/api/auth/login', json={
        'username': 'logintest',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'error' in response.json

    # Test login with non-existent user
    response = client.post('/api/auth/login', json={
        'username': 'nonexistentuser',
        'password': 'somepassword'
    })
    assert response.status_code == 401
    assert 'error' in response.json
