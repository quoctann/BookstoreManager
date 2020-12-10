from functools import wraps
from flask import session, request, redirect, url_for
from flask_login import current_user


def login_required_cart(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login?next=/cart')

        return f(*args, **kwargs)

    return decorated_function


def login_required_wishlist(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login?next=/wishlist')

        return f(*args, **kwargs)

    return decorated_function

