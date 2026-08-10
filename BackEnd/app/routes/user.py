from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timezone, timedelta

from ..models import Recipe, User
from ..extensions import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
@login_required
def get_user():
    return jsonify({
        'hello':f'hello user number {current_user.user_id}'
    })