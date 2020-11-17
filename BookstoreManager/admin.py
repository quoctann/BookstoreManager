from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect
from BookstoreManager import admin, db
from BookstoreManager.models import *
from flask_login import current_user, logout_user


# Khi đăng nhập mới xem được view này, dùng cho view tùy chỉnh
class AuthenticatedView(BaseView):
    __abstract__ = True

    def is_accessible(self):
        return current_user.is_authenticated


# Như trên nhưng dùng cho view của model
class ModelAuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class SellingBookView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/selling-book.html')


class LogoutView(AuthenticatedView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")


admin.add_view(SellingBookView(name='Bán sách'))
admin.add_view(ModelAuthenticatedView(SystemUser, db.session, name="Quản lý người dùng"))
admin.add_view(ModelAuthenticatedView(BookStorage, db.session))
admin.add_view(ModelAuthenticatedView(BookImport, db.session))
admin.add_view(LogoutView(name="Đăng xuất"))

