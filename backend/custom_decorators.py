from functools import wraps
from flask.helpers import url_for
from flask_login import current_user
from flask import redirect


def permissions_required(*perm_args):
    if len(perm_args) <= 0:
        raise ValueError("Must provide at least one access level")

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in perm_args:
                if isinstance(arg, str):
                    if not current_user.permissions == arg:
                        return redirect(url_for('home.home_page'))
                elif isinstance(arg, list):
                    if not any(current_user.permissions == perm for perm in arg):
                        return redirect(url_for('home.home_page'))
            return func(*args, **kwargs)
        return wrapper
    return decorator
