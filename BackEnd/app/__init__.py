from flask import Flask
from flask import jsonify
from flask_wtf.csrf import CSRFError
from .extensions import db, migrate, login_manager, csrf
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# What is CORS? https://www.geeksforgeeks.org/python/how-to-install-flask-cors-in-python/
from flask_cors import CORS

# Explicitly load FoodApp/BackEnd/.env in any working directory
backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=backend_dir / ".env.local", override=True)
load_dotenv(dotenv_path=backend_dir / ".env", override=False)

def create_app(test_config=None):
    app = Flask(__name__)
    # update methods as neeeded,

    # Change to "production" in .env file when app is in production, otherwise it's "development"
    is_prod = os.environ.get("FLASK_ENV") == "production"
    samesite = "None" if is_prod else "Lax"

    # Read Neon connecttion string from .env falling back to local db file
    db_uri = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite')
    if db_uri.startswith('postgres://'):
        db_uri = db_uri.replace('postgres://', 'postgresql://', 1)

    # Default Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_recycle": 300,
    }

    # Cookies
    app.config.update(
        FRONTEND_ORIGIN=os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173"),
        # Session cookies
        SESSION_COOKIE_HTTPONLY = True,
        SESSION_COOKIE_SECURE=is_prod,
        SESSION_COOKIE_SAMESITE=samesite,
        PERMANENT_SESSION_LIFETIME=timedelta(days=7),

        # Remember me cookies
        REMEMBER_COOKIE_SAMESITE="None",
        REMEMBER_COOKIE_SECURE=is_prod,
        REMEMBER_COOKIE_HTTPONLY=samesite,
        REMEMBER_COOKIE_DURATION=timedelta(days=7),

        # CSRF: tokens come from /csrf route in login.py, they are sent in X-CSRF-Token
        WTF_CSRF_HEADERS=["X-CSRF-Token"],
        WTF_CSRF_TIME_LIMIT=None,
        WTF_CSRF_SSL_STRICT=is_prod,
    )

    # == = = = = = = = = = = = = = =
    # Override defaults if for testing purposes
    if test_config is not None:
        app.config.update(test_config)
    # = = = = = = = = = = = = = = = 

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    login_manager.init_app(app)
    csrf.init_app(app)

    CORS(
        app, 
        origins=[os.environ.get("FRONTEND_ORIGIN")],
        supports_credentials=True, 
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "X-CSRF-Token"],
    )

    @login_manager.unauthorized_handler
    def unauthorized():
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

    @app.errorhandler(CSRFError)
    def handle_CSRFError(e):
        return jsonify({
            "error": "CSRF validation failed",
            "detail": e.description,
        }), 400

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