from functools import wraps
from flask import jsonify
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Must be logged in
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401

        # Must have is_admin set to True
        if not getattr(current_user, 'is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403

        return f(*args, **kwargs)
    return decorated_function