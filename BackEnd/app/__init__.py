from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from flask_migrate import Migrate

# What is CORS? https://www.geeksforgeeks.org/python/how-to-install-flask-cors-in-python/
from flask_cors import CORS


# Initialize SQLAlchemy instance (outside create_app for import access)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # update methods as neeeded,
    CORS(app, supports_credentials=True, methods=["GET", "POST"])

    # Configuration
    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Configure Flask-Login
    login_manager = LoginManager()
    # this redirect unathenticated users to a page, put in login.login for name of your blueprint, and then the url
    login_manager.login_view = 'login.login'
    login_manager.init_app(app)

    # User loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Register blueprints
    from .routes.main import main_bp
    app.register_blueprint(main_bp)

    from .routes.signup import signup_db
    app.register_blueprint(signup_db)

    from .routes.login import login_bp
    app.register_blueprint(login_bp)

    from .routes.recipes import recipes_db
    app.register_blueprint(recipes_db)

    return app