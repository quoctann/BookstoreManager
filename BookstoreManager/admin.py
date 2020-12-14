from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect, url_for, request, session
from BookstoreManager import admin, db, utils
from BookstoreManager.models import *
from flask_login import current_user, logout_user


# |============|
# | VIEW CƠ SỞ |
# |============|


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


# View dùng cho việc đăng xuất
class LogoutView(AuthenticatedView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")


# |=============|
# | VIEW TÁC VỤ |
# |=============|


# |--------------------------------------------|
# | Các view tác vụ thông thường của nhân viên |
# |--------------------------------------------|


class SellView(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/sell.html',
                           valid_debt=session['valid_debt'],
                           sell_for=session['sell_for'])


class ImportView(AuthenticatedView):
    @expose('/')
    def index(self):
        books = BookStorage.query.all()
        quantity, price = utils.import_stats(session.get('import_book'))
        import_info = {
            "total_amount": price,
            "total_quantity": quantity
        }
        return self.render('admin/task_view/import.html', books=books, import_info=import_info)


class SubmitImportView(AuthenticatedView):
    @expose('/')
    def index(self):
        quantity, price = utils.import_stats(session.get('import_book'))
        import_info = {
            "total_amount": price,
            "total_quantity": quantity
        }
        return self.render('admin/task_view/submit-import.html', import_info=import_info)


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


# |------------------------------------------|
# | Các view tác vụ chỉ admin được thực hiện |
# |------------------------------------------|

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


# |------------------|
# | Các view phụ trợ |
# |------------------|
class ExportInvoice(AuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/task_view/export_invoice.html')


# |=========================|
# | THÊM VIEW VÀO TRANG CHỦ |
# |=========================|


# Tác vụ
admin.add_view(SellView(name="Bán sách"))
admin.add_view(DebtCollectionView(name="Thu nợ"))
admin.add_view(ReportView(name="Báo cáo"))
admin.add_view(ImportView(name="Nhập sách"))
admin.add_view(SubmitImportView(name="Xác nhận đơn nhập sách"))
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
admin.add_view(ExportInvoice(name='Xuất hóa đơn'))
admin.add_view(RegisterView(name='Thêm nhân viên'))
admin.add_view(RuleView(name='Đổi quy định'))
admin.add_view(LogoutView(name="Đăng xuất"))
