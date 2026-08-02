from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from .. import db

signup_db = Blueprint('signup', __name__, template_folder="templates")

@signup_db.route("/signup")
def signup():
    return render_template('signup.html')

@signup_db.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('An account with this email address already exists')
        return redirect(url_for('signup.signup'))

    # create new user. Hash password so plaintext version never stored
    new_user = User(email=email, name=name, password=generate_password_hash(password))

    # add user to db
    db.session.add(new_user)
    db.session.commit()

    # insert proper login route when done
    return redirect(url_for('login.login'))