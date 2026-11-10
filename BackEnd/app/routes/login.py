import secrets
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import login_user, login_required, logout_user
from sqlalchemy import select
from ..models import User
from ..extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta, timezone
import re

login_bp = Blueprint('login', __name__, template_folder='templates')

def is_email(email):
    """
    Checks if input is an email that is RFC 5322 compliant

    Param: email (str)
    Returns: boolean
    """
    EMAIL_REGEX = re.compile(r"^(?P<local>[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+)@(?P<domain>[A-Za-z0-9.-]+\.[A-Za-z]{2,})$")

    # Will return true if a valid email is inputted, false otherwise
    return EMAIL_REGEX.match(email) is not None

@login_bp.route('/login', methods=['POST'])
def login_post():
    """
    Log a user in and start a session.

    Auth: public
    Body: email (str), password (str)
    Returns: 200: {message}, sets session cookie
    Errors: 400: bad JSON, missing fields, unknown email, wrong password
    """

    data = request.get_json()

    # Check valid JSON format
    if not isinstance(data, dict): 
        return jsonify({
            "error": "Request body must be valid JSON"
        }), 400

    username = data.get("username")
    password = data.get("password")
    # Check whether or not user wants to be remembered and not have to login again when reopening page
    # remember = bool(request.form.get('remember'))

    # If email/username or password are missing
    if not username or not password:
        return jsonify({
            "error": "Missing either username or password"
        }), 400

    # Checking whether a username or email was inputted
    if is_email(username):
        email = username

        # Querying the database using the email inputted
        stmt = select(User).filter_by(email=email)
        existing_user = db.session.scalars(stmt).first()
    # If a username was inputted
    else:
        stmt = select(User).filter_by(name=username)
        existing_user = db.session.scalars(stmt).first()

    # Checking to see if a user does not exist in the database with that email
    if not existing_user:
        return jsonify({
            "error": "Nonexisting user, please sign up first"
        }), 400

    # Checking to see if a user with that email already exists in the database
    if not check_password_hash(existing_user.password, password):
        return jsonify({
            "error":"Incorrect password, please try again"
        }), 400

    # Clear old session data
    session.clear()
    
    # remember default true for testing
    login_user(existing_user, remember=True)
    session["user_id"] = existing_user.get_id()
    
    return jsonify({
        "message":"Successful login"
    }), 200

@login_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """
    Generate a 1-hour password reset token and store it on the user.

    Auth: public
    Body: email (str)
    Returns: 200: {message}. No email is sent yet
    Errors: 400: missing body/email, user not found
    """
    data = request.get_json()

    if not data: 
        return jsonify({
            "error": "Missing JSON body"
        }), 400

    email = data["email"]

    if not email:
        return jsonify({
            "error":"Missing email"
        }), 400

    stmt = select(User).filter_by(email=email)
    existing_user = db.session.scalars(stmt).first()

    if existing_user:

        # Generating token that will go in reset password url
        token = secrets.token_urlsafe(32)
        existing_user.reset_token = token
        existing_user.reset_token_expires = (datetime.now(timezone.utc) + timedelta(minutes=30))
        db.session.commit()

        # For testing purposes, will replace with an email sending service
        reset_link = f"http://localhost:5173/reset-password?token={token}"

        print(f"Password reset link: {reset_link}")

    return jsonify({
        "message":"If an account exist with that email, a password reset link has been sent."
    }), 200


@login_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """
    Set a new password using a reset token from the URL.

    Auth: public
    Body: email (str), password (str)
    Returns: 200: {message}; token is cleared after use
    Errors: 400: missing email/password, invalid or expired token
    """

    data = request.get_json()

    new_password = data.get("password")
    token = data.get("token")

    if not new_password:
        return jsonify({
            "error":"New password can't be empty."
        }), 400
    elif len(new_password) < 8:
        return jsonify({
            "error": "Password must be longer than 8 characters."
        }), 400

    user = User.query.filter_by(reset_token=token).first()

    if not user or user.reset_token != token:
        return jsonify({
            "error": "Invalid reset token."
        }), 400

    # print("User token expires ", user.reset_token_expires)
    # print("The time is ", datetime.now(timezone.utc))

    expires = user.reset_token_expires.replace(tzinfo=timezone.utc)

    if expires < datetime.now(timezone.utc):
        return jsonify({
            "error":"Reset token has expired."
        }), 400

    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password

    # Reset token so it can't be reused
    user.reset_token = None
    user.reset_token_expires = None

    db.session.commit()

    return jsonify({
        "message":"Your password has been successfully reset."
    }), 200

@login_bp.route('/logout')
@login_required
def logout():
    """
    End the current session.

    Auth: login required
    Returns: 200: {message}
    """
    logout_user()
    return jsonify({
        "message":"Successful logout"
    }), 200