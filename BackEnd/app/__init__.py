from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from .routes.helloworld import helloworld_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # Register blueprint
    app.register_blueprint(helloworld_bp)

    return app