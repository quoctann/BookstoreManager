from BookstoreManager import app, db
from BookstoreManager.models import SystemUser
import hashlib


def add_admin(name, username, password):
    user = SystemUser(name=name, username=username,
                      password=str(hashlib.md5(password.strip().encode("utf-8")).hexdigest()))
    db.session.add(user)
    db.session.commit()

    return user