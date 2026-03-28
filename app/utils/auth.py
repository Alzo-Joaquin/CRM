from functools import wraps
from flask import jsonify
from flask_login import current_user


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({"error": "No autenticado"}), 401

            if current_user.rol not in roles:
                return jsonify({"error": "No autorizado"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator