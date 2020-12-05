from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect
from BookstoreManager import admin, db
from BookstoreManager.models import *
from flask_login import current_user, logout_user


# Tùy chỉnh view

# Tùy chỉnh lại model view cho phù hợp với layout
class CustomModelView(ModelView):
    list_template = 'admin/model/model_list.html'
    create_template = 'admin/model/model_create.html'
    edit_template = 'admin/model/model_edit.html'
    can_delete = False
    can_edit = False
    can_create = False
    can_export = False
    column_exclude_list = ['password', ]


# Khi đăng nhập mới xem được view này, dùng cho view tùy chỉnh
class AuthenticatedView(BaseView):
    __abstract__ = True

    def is_accessible(self):
        return current_user.is_authenticated


# Khi đăng nhập mới xem được view này, dùng cho view của model
class ModelAuthenticatedView(CustomModelView):
    def is_accessible(self):
        return current_user.is_authenticated


# View của form đăng ký thêm nhân viên
class RegisterView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/register.html')


# View dùng cho việc đăng xuất
class LogoutView(AuthenticatedView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")


# Các view của tác vụ
class SellView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/sell.html')


class ImportView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/import.html')


class DebtCollectionView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/debt_collection.html')


class ReportView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/report.html')


class StorageView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/storage.html')


class CustomerView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/customer.html')


# Thêm view vào trang chủ
# Tác vụ
admin.add_view(SellView(name="Bán sách"))
admin.add_view(DebtCollectionView(name="Thu nợ"))
admin.add_view(ReportView(name="Báo cáo"))
admin.add_view(ImportView(name="Nhập sách"))
admin.add_view(StorageView(name="Xem kho"))
admin.add_view(CustomerView(name="Khách hàng"))
admin.add_view(ModelAuthenticatedView(BookStorage, db.session,
                                      category="Xem dữ liệu thô",
                                      name="Kho sách"))
admin.add_view(ModelAuthenticatedView(Customer, db.session,
                                      category="Xem dữ liệu thô",
                                      name="Khách hàng"))
admin.add_view(ModelAuthenticatedView(InvoiceDetail, db.session,
                                      category="Xem dữ liệu thô",
                                      name="Hóa đơn"))
# Tính năng bổ sung
admin.add_view(RegisterView(name='Thêm nhân viên'))
admin.add_view(LogoutView(name="Đăng xuất"))


