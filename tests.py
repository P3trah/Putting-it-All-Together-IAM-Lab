# tests.py

import pytest
from app import create_app, db
from app.models import User, Recipe

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup(client):
    # Test sign-up feature
    response = client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpassword',
        'image_url': 'https://example.com/image.jpg',
        'bio': 'Test bio'
    })
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['username'] == 'testuser'
    assert response.json['image_url'] == 'https://example.com/image.jpg'
    assert response.json['bio'] == 'Test bio'

def test_login(client):
    # Test login feature
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['username'] == 'testuser'

def test_logout(client):
    # Test logout feature
    response = client.delete('/logout')
    assert response.status_code == 204

def test_auto_login(client):
    # Test auto-login feature
    response = client.get('/check_session')
    assert response.status_code == 200
    assert 'id' in response.json
    assert response.json['username'] == 'testuser'

def test_recipe_view(client):
    # Test recipe viewing feature
    response = client.get('/recipes')
    assert response.status_code == 401  # Unauthorized without login

def test_recipe_creation(client):
    # Test recipe creation feature
    client.post('/signup', json={
        'username': 'testuser',
        'password': 'testpassword',
        'image_url': 'https://example.com/image.jpg',
        'bio': 'Test bio'
    })
    client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    response = client.post('/recipes', json={
        'title': 'Test Recipe',
        'instructions': 'Lorem ipsum dolor sit amet.',
        'minutes_to_complete': 30
    })
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['title'] == 'Test Recipe'
    assert response.json['instructions'] == 'Lorem ipsum dolor sit amet.'
    assert response.json['minutes_to_complete'] == 30
