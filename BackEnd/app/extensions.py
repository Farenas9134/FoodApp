from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


# Initialize SQLAlchemy instance (outside create_app for import access)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()