from flask import Flask
from .routes.helloworld import helloworld_bp

def create_app():
    app = Flask(__name__)

    # Register blueprint
    app.register_blueprint(helloworld_bp)

    return app