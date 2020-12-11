from functools import wraps
from flask import session, request, redirect, url_for
from flask_login import current_user


# Xác thực trạng thái đăng nhập phía client
def client_login_required(f):
    @wraps(f)
    def check_login(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("login_customer", next=request.url))

        return f(*args, **kwargs)

    return check_login


# Check trạng thái đăng nhập ở giỏ hàng
def login_required_cart(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login?next=/cart')

        return f(*args, **kwargs)

    return decorated_function


# Check trạng thái đăng nhập ở danh sách yêu thích
def login_required_wishlist(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login?next=/wishlist')

        return f(*args, **kwargs)

    return decorated_function

