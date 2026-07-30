from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint("main" , __name__, template_folder='templates')

@main_bp.route("/")
def home():
    return render_template('main.html')

@main_bp.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
