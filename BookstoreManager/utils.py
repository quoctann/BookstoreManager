from flask import session
from BookstoreManager import app, db
from BookstoreManager.models import SystemUser
import hashlib


def add_admin(name, username, password):
    user = SystemUser(name=name, username=username,
                      password=str(hashlib.md5(password.strip().encode("utf-8")).hexdigest()))
    db.session.add(user)
    db.session.commit()

    return user


def reset_value():
    session['valid_debt'] = 'init'
    # Session lưu thuộc tính nhân viên đã kiểm tra nợ của KH chưa
    session['debt_checking_status'] = 'init'
    # Lưu tạm thời tên của khách hàng
    session['sell_for'] = 'init'


class TaskRules:
    pass
