from flask import Flask
from flask import jsonify
from .extensions import db, migrate, login_manager
import os
from pathlib import Path
from dotenv import load_dotenv

# What is CORS? https://www.geeksforgeeks.org/python/how-to-install-flask-cors-in-python/
from flask_cors import CORS

# Explicitly load FoodApp/BackEnd/.env in any working directory
backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=backend_dir / ".env.local", override=True)
load_dotenv(dotenv_path=backend_dir / ".env", override=False)

def create_app(test_config=None):
    app = Flask(__name__)
    # update methods as neeeded,
    CORS(app, supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE"])

    # Read Neon connecttion string from .env falling back to local db file
    db_uri = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
    if db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://', 1)

    # Defualt Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    # == = = = = = = = = = = = = = =
    # Override defaults if for testing purposes
    if test_config is not None:
        app.config.update(test_config)
    # = = = = = = = = = = = = = = = 

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unathorized():
        return {
            "error": "Authentication required",
            "message":"Please log in first."
        }, 401

    # User loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # App-wide error handler to return json formatted errors instead of default html
    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({
            "error": getattr(e, "description", "Resource not found")
        }), 404

    # Register blueprints
    from .routes.signup import signup_db
    app.register_blueprint(signup_db, url_prefix='/api')

    from .routes.login import login_bp
    app.register_blueprint(login_bp, url_prefix='/api')

    from .routes.recipes import recipes_db
    app.register_blueprint(recipes_db, url_prefix='/api')

    from .routes.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    from .routes.ingredients import ingredient_bp
    app.register_blueprint(ingredient_bp, url_prefix='/api')

    from .routes.pantry import user_pantry_bp
    app.register_blueprint(user_pantry_bp, url_prefix='/api')

    return app