from flask import Blueprint, render_template

helloworld_bp = Blueprint("helloworld", __name__)

@helloworld_bp.route("/")
def index():
    return "Hello World!"

@helloworld_bp.route("/hello/<name>")
def hello_name(name):
    return f"Hello {name}!"