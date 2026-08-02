from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager

# Initialize SQLAlchemy instance (outside create_app for import access)
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    # Initialize extensions with app
    db.init_app(app)

    # Configure Flask-Login
    login_manager = LoginManager()
    # this redirect unathenticated users to a page, put in login.login for name of your blueprint, and then the url
    login_manager.login_view = 'login.login'
    login_manager.init_app(app)

    # User loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    from .routes.signup import signup_db
    app.register_blueprint(signup_db)

    return app