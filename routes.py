from flask import request, jsonify, session
from .models import db, User, Recipe
from . import app

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    image_url = data.get('image_url')
    bio = data.get('bio')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 422

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 422

    user = User(username=username, password=password, image_url=image_url, bio=bio)
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    return jsonify({'user_id': user.id, 'username': user.username, 'image_url': user.image_url, 'bio': user.bio}), 201

@app.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return jsonify({'user_id': user.id, 'username': user.username, 'image_url': user.image_url, 'bio': user.bio}), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    session['user_id'] = user.id
    return jsonify({'user_id': user.id, 'username': user.username, 'image_url': user.image_url, 'bio': user.bio}), 200

@app.route('/logout', methods=['DELETE'])
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        return '', 204
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/recipes', methods=['GET'])
def get_recipes():
    if 'user_id' in session:
        recipes = Recipe.query.all()
        return jsonify([{'title': recipe.title, 'instructions': recipe.instructions, 'minutes_to_complete': recipe.minutes_to_complete, 'user': {'username': recipe.user.username}} for recipe in recipes]), 200
    else:
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/recipes', methods=['POST'])
def create_recipe():
    if 'user_id' in session:
        data = request.json
        title = data.get('title')
        instructions = data.get('instructions')
        minutes_to_complete = data.get('minutes_to_complete')

        if not title or not instructions or not minutes_to_complete:
            return jsonify({'error': 'Title, instructions, and minutes_to_complete are required'}), 422

        recipe = Recipe(title=title, instructions=instructions, minutes_to_complete=minutes_to_complete, user_id=session['user_id'])
        db.session.add(recipe)
        db.session.commit()

        return jsonify({'title': recipe.title, 'instructions': recipe.instructions, 'minutes_to_complete': recipe.minutes_to_complete, 'user': {'username': recipe.user.username}}), 201
    else:
        return jsonify({'error': 'Unauthorized'}), 401
