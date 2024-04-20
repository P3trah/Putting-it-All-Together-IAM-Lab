# app.py or __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Import blueprints
    from .auth.routes import auth_bp
    from .recipes.routes import recipes_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipes_bp)

    return app
