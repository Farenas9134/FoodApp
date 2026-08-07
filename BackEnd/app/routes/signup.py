from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from ..models import User
from ..extensions import db

signup_db = Blueprint('signup', __name__)

# @signup_db.route("/signup")
# def signup():
#     return render_template('signup.html')

@signup_db.route('/signup', methods=['POST'])
def signup_post():

    data = request.get_json()

    if not data: 
        return jsonify({"error": "Missing JSON body"}), 400

    email = data["email"]
    name = data["name"]
    password = data["password"]

    if not email or not password or not name:
        return jsonify({
            "error":"Missing required fields"
        }), 400

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({
            "error": "Email attached to existing user."
        }), 400

    # create new user. Hash password so plaintext version never stored
    new_user = User(email=email, name=name, password=generate_password_hash(password))

    # add user to db
    db.session.add(new_user)
    db.session.commit()

    # return successful json message
    return jsonify({
        "message":"User created successfully",
        "user":{
            "email": email,
            "name": name
        }
    })

@signup_db.route('/signup-test')
def signup_test():
    return 'Hahaha you have curl working!'