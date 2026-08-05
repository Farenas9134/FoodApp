from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from ..models import User
from werkzeug.security import check_password_hash

login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login')
def login():
    return render_template('login.html')

'''
Gets a user's username and password, queries the user database to determine whether the user has signed up; if yes, successful login follows
'''
@login_bp.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    # Check whether or not user wants to be remembered and not have to login again when reopening page
    remember = bool(request.form.get('remember'))

    user = User.query.filter_by(email=email).first()

    # Checking if user exists
    if not user or not check_password_hash(user.password, password):
        flash('Incorrect login details please try again')
        # Reload page if password is wrong or does not exist
        return redirect(url_for('login.login'))

    # Successful login
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

'''
Logs out a user from their current session
'''
@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))