import secrets
import re
import hashlib

from flask import Blueprint, request, jsonify, session, current_app
from flask_wtf.csrf import generate_csrf
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select
from ..models import User
from ..extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta, timezone


login_bp = Blueprint('login', __name__, template_folder='templates')

EMAIL_REGEX = re.compile(
    r"^(?P<local>[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+)@(?P<domain>[A-Za-z0-9.-]+\.[A-Za-z]{2,})$"
    )
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
RESET_TOKEN_MINUTES = 30

# Don't want to give away when a user exists or not so this is checked when a user doesn't exist so response time doesn't give that away
DUMMY_HASH = generate_password_hash("fake-password")

def is_email(email):
    """
    Checks if input is an email that is RFC 5322 compliant

    Param: email (str)
    Returns: boolean
    """

    # Will return true if a valid email is inputted, false otherwise
    return EMAIL_REGEX.match(email) is not None

def json_body():
    """
    Returns a JSON body if the data is a JSON instance, otherwise None so no errors
    get raised
    """

    data = request.get_json(silent=True)

    if isinstance(data, dict):
        return data
    else:
        return None

def hash_token(token):
    """
    Used so we don't store the raw token in the database

    Param: token (str)
    Returns: hashed token (str)
    """
    return hashlib.sha256(token.encode()).hexdigest()

def user_payload(user):
    """
    Returns details of a user
    """

    return {"id": user.get_id(), "name": user.name, "email": user.email}

@login_bp.route('/csrf', methods=['GET'])
def give_csrf_token():
    """
    Generates a CSRF (Cross-Site Request Forgery) token tied to current session
    cookie

    Ref: https://brightsec.com/blog/csrf-token/#what-is-csrf-token
    CSRF tokens are server generated values embedded in web forms or requests that are used to verify authenticity of a user's 
    request. When a user submits a form, the server compares the CSRF token with the stored token to ensure they are the same.
    These tokens prevent attackers from performing actions on behalf of logged in users. The tokens should always be transmitted through
    POST, PUT, or DELETE methods and never GET methods as this makes the token accessible via the URL.

    Auth: public
    Params: None
    Returns: 200: {csrf_token}, issues a session CSRF token
    """
    return jsonify({
        "csrf_token": generate_csrf()
    }), 200

@login_bp.route('/me', methods=["GET"])
@login_required
def me():
    """
    Returns the current logged-in user. Frontend will call this to ensure the session cookie is still valid.

    Auth: login required
    Params: None
    Returns: 200: {user}, logged-in user
    """

    return jsonify({
        "user": user_payload(current_user)
    }), 200

@login_bp.route('/login', methods=['POST'])
def login_post():
    """
    Log a user in and start a session.

    Auth: public
    Body: email (str), password (str)
    Returns: 200: {message}, sets session cookie
    Errors: 400: bad JSON, missing fields, unknown email, wrong password
    """

    data = json_body()

    # Check valid JSON format
    if data is None: 
        return jsonify({
            "error": "Request body must be valid JSON"
        }), 400

    username = data.get("username")
    password = data.get("password")
    # Check whether or not user wants to be remembered and not have to login again when reopening page
    remember = data.get("remember") is True

    # If email/username or password are missing
    if not isinstance(username,str) or not isinstance(password, str) or not username.strip() or not password:
        return jsonify({
            "error": "Missing username or password."
        }), 400

    # Getting rid of trailing/leading whitespace
    username = username.strip()

    # Checking whether a username or email was inputted
    if is_email(username):
        email = username.lower()

        # Querying the database using the email inputted
        stmt = select(User).filter_by(email=email)
    # If a username was inputted
    else:
        stmt = select(User).filter_by(name=username)

    user = db.session.scalars(stmt).first()

    # Checking password whether or not user actually exists as runtime difference can leak whether a user exists
    if user:
        password_ok = check_password_hash(user.password)
    else:
        password_ok = check_password_hash(DUMMY_HASH, password[:MAX_PASSWORD_LENGTH])

    # Returning a generic message so attackers can't tell which accounts exist
    if not user or not password_ok or not user.is_active:
        return jsonify({
            "error": "Invalid username or password."
        }), 401

    # Clear old session data including previous CSRF token
    session.clear()
    
    # remember default true for testing
    login_user(user, remember=True)
    session["user_id"] = user.get_id()
    session.permanent = remember
    
    return jsonify({
        "message":"Successful login",
        "user": user_payload(user),
        "csrf_token": generate_csrf(),
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
    data = json_body()

    if data: 
        email = data.get("email")
    else:
        email = None

    if not isinstance(email, str) or not email.strip():
        return jsonify({
            "error":"Missing email"
        }), 400

    stmt = select(User).filter_by(email=email.strip().lower())
    user = db.session.scalars(stmt).first()

    if user:
        # Generating token that will go in reset password url
        token = secrets.token_urlsafe(32)
        # Encode token in case of leaks
        user.reset_token = hash_token(token)
        user.reset_token_expires = (datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_MINUTES))
        db.session.commit()

        frontend = current_app.config.get("FRONTEND_ORIGIN", "https://localhost:5173")
        print(f"Password reset link: {frontend}/reset-password?token={token}")

        # For testing purposes, will replace with an email sending service
        # reset_link = f"http://localhost:5173/reset-password?token={token}"
        # print(f"Password reset link: {reset_link}")

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

    data = json_body()

    if data is None:
        return jsonify({
            "error": "Request body must be valid JSON"
        }), 400

    new_password = data.get("password")
    token = data.get("token")

    if not isinstance(token, str) or not token:
        return jsonify({
            "error": "Invalid reset token."
        }), 400

    # Checking password requirements
    if not isinstance(new_password, str) or len(new_password) < MIN_PASSWORD_LENGTH:
        return jsonify({
            "error": f"New password must be at least {MIN_PASSWORD_LENGTH} characters."
        }), 400
    if len(new_password) > MAX_PASSWORD_LENGTH:
        return jsonify({
            "error": f"Password must be at most {MAX_PASSWORD_LENGTH} characters."
        }), 400

    stmt = select(User).filter_by(reset_token=hash_token(token))
    user = db.session.scalars(stmt).first()

    if not user or user.reset_token is None:
        return jsonify({
            "error": "Invalid reset token."
        }), 400

    expires = user.reset_token_expires

    # Handling naive datetimes
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

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

@login_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    End the current session.

    Auth: login required
    Returns: 200: {message}
    """
    logout_user()
    session.clear()
    return jsonify({
        "message":"Successful logout",
        "csrf_token": generate_csrf()
    }), 200