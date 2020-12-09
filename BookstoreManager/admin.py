from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect, url_for, request, session
from BookstoreManager import admin, db
from BookstoreManager.models import *
from flask_login import current_user, logout_user


# VIEW CƠ SỞ
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


# View của nhân viên
# Khi đăng nhập mới xem được view này, dùng cho view tùy chỉnh
class AuthenticatedView(BaseView):
    __abstract__ = True

    def is_accessible(self):
        return current_user.is_authenticated


# Khi đăng nhập mới xem được view này, dùng cho view của model
class ModelAuthenticatedView(CustomModelView):
    def is_accessible(self):
        return current_user.is_authenticated


# View dùng cho việc đăng xuất
class LogoutView(AuthenticatedView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")


# VIEW TÁC VỤ
# Các view của tác vụ thông thường
class SellView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/sell.html', valid_debt=session['valid_debt'], sell_for=session['sell_for'])


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


# VIEW ADMIN
# Template thông thường
class AdminView(AuthenticatedView):
    def is_accessible(self):
        # return current_user.is_authenticated        # change
        return current_user.is_authenticated and current_user.role == 'Admin'


# Model view dành riêng cho admin
class AdminModelView(CustomModelView):
    def is_accessible(self):
        # return current_user.is_authenticated        # change
        return current_user.is_authenticated and current_user.role == 'Admin'

# View của form đăng ký thêm nhân viên
class RegisterView(AdminView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/register-employee.html')


# View để admin xem, thay đổi quy định
class RuleView(AdminView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/rule.html')


# Admin thao tác với bảng
class CanCreate(AdminModelView):
    can_create = True
    column_display_pk = True


# THÊM VIEW VÀO TRANG CHỦ
# Tác vụ
admin.add_view(SellView(name="Bán sách"))
admin.add_view(DebtCollectionView(name="Thu nợ"))
admin.add_view(ReportView(name="Báo cáo"))
admin.add_view(ImportView(name="Nhập sách"))
admin.add_view(StorageView(name="Xem kho"))
admin.add_view(CustomerView(name="Khách hàng"))
admin.add_view(AdminModelView(BookStorage, db.session,
                              category="Xem dữ liệu thô",
                              name="Kho sách"))
admin.add_view(CanCreate(Customer, db.session,
                         category="Xem dữ liệu thô",
                         name="Khách hàng"))
admin.add_view(AdminModelView(InvoiceDetail, db.session,
                              category="Xem dữ liệu thô",
                              name="Hóa đơn"))
# Tính năng bổ sung
admin.add_view(RegisterView(name='Thêm nhân viên'))
admin.add_view(RuleView(name='Đổi quy định'))
admin.add_view(LogoutView(name="Đăng xuất"))