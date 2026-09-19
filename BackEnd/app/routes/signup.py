from flask import Blueprint, request, jsonify
from sqlalchemy import select
from werkzeug.security import generate_password_hash
from ..models import User
from ..extensions import db

signup_db = Blueprint('signup', __name__)

@signup_db.route('/signup', methods=['POST'])
def signup_post():

    data = request.get_json(silent=True)

    if not isinstance(data, dict): 
        return jsonify({"error": "Request body must be valid JSON"}), 400

    email = data.get("email")
    name = data.get("name")
    password = data.get("password")

    if not email or not password or not name:
        return jsonify({
            "error":"Missing required fields"
        }), 400

    """
        Doing a Select query everytime can be slow & lead to a "race" where user's A & B submit
        a request at the same time, and they both get hit with a blank page.
        Solution: Attempt to commit without the check, and if an error is thrown, just rollback. A unique constraint is crucial for this to work
    """
    # stmt = select(User).filter_by(email=email)
    # existing_user = db.session.scalars(stmt).first()

    # if existing_user:
    #     return jsonify({
    #         "error": "Email attached to existing user."
    #     }), 400

    # create new user. Hash password so plaintext version never stored
    new_user = User(email=email, name=name)
    new_user.set_password(password)

    # add user to db
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": "Email attached to existing user."}), 400

    # return successful json message
    return jsonify({
        "message":"User created successfully",
        "user":{
            "email": email,
            "name": name
        }
    }), 201