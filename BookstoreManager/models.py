from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from BookstoreManager import db
from flask_login import UserMixin
from datetime import datetime


# |==================================|
# | MODEL TRỪU TƯỢNG, TRÁNH LẶP CODE |
# |==================================|


# Các thông tin thông dụng như id, name dùng chung
class CommonIdentityBase(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    avatar = Column(String(50))


# Các thông tin hỗ trợ việc xác thực như username, password
class AuthIndentityBase(db.Model, UserMixin):
    __abstract__ = True
    username = Column(String(20), nullable=False)
    password = Column(String(40), nullable=False)
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name


# |=============================|
# | MODEL CHÍNH MÔ TẢ NGHIỆP VỤ |
# |=============================|


# Danh sách tài khoản đăng nhập (demo)
# class SystemUser(CommonIdentityBase, AuthIndentityBase):
#     __tablename__ = 'system_user'
#     role = Column(String(10), nullable=False, default='Employee')


# Thông tin nhân viên và vai trò trong hệ thống
class Employee(CommonIdentityBase, AuthIndentityBase):
    __tablename__ = 'employee'
    avatar = Column(String(50), default='images/admin/su.png')
    role = Column(String(10), nullable=False, default='Employee')
    # Chịu trách nhiệm cho nhiều phiếu thu nợ
    collect_debt = relationship('DebtCollection', backref='employee', lazy=True)
    # Chịu trách nhiệm cho nhiều phiếu nhập sách
    in_charged = relationship('BookImport', backref='employee', lazy=True)
    # Chịu trách nhiệm cho nhiều hóa đơn bán sách
    create_invoice = relationship('Invoice', backref='employee', lazy=True)


# Thông tin khách hàng
class Customer(CommonIdentityBase, AuthIndentityBase):
    __tablename__ = 'customer'
    email = Column(String(40), nullable=False)
    address = Column(String(100))
    phone = Column(Integer)
    role = Column(String(10), nullable=False, default='guest')
    # Lưu số nợ hiện tại
    debt = Column(Integer, default=0)
    # Đã trả những khoản nợ nào
    paid_debt = relationship('DebtCollection', backref='customer', lazy=True)
    # Có những hóa đơn nào
    paid_invoice = relationship('Invoice', backref='customer', lazy=True)
    # Mỗi khách hàng có yêu thích riêng
    wish_id = relationship('WishDetail', backref='customer', lazy=True)


# Dữ liệu khi nhân viên thu nợ khách hàng
class DebtCollection(db.Model):
    __tablename__ = 'debt_collection'
    debt_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    date = Column(Date, default=datetime.today(),  nullable=False)
    amount = Column(Float, nullable=False)


# Thông tin sách trong kho
class BookStorage(CommonIdentityBase):
    __tablename__ = 'book_storage'
    instock = Column(Integer, nullable=False)
    author = Column(String(30), nullable=False)
    category = Column(String(20), nullable=False)
    selling_price = Column(Integer, nullable=False)
    path = Column(String(50), default='images/defaultbook.jpg')
    # Sách được nhập bởi những đơn hàng nào
    imported_by = relationship('ImportDetail', backref='book_storage', lazy=True)
    # Sách được bán trên những hóa đơn nào
    sold_invoice = relationship('InvoiceDetail', backref='book_storage', lazy=True)
    # Sách yêu thích của khách hàng được truy vấn lấy dữ liệu từ khóa ngoại này
    wish_id = relationship('WishDetail', backref='book_storage', lazy=True)


# Thông tin phiếu nhập sách
class BookImport(db.Model):
    __tablename__ = 'book_import'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, default=datetime.today())
    total_cost = Column(Float, nullable=False)
    # Nhân viên chịu trách nhiệm nhập sách
    employee_incharge = Column(Integer, ForeignKey(Employee.id))
    # 1 phiếu nhập có thông tin nhiều sách
    import_detail = relationship('ImportDetail', backref='book_import', lazy=True)


# Thông tin chi tiết về phiếu nhập sách
class ImportDetail(db.Model):
    __tablename__ = 'import_detail'
    book_id = Column(Integer, ForeignKey(BookStorage.id), primary_key=True, nullable=False)
    import_id = Column(Integer, ForeignKey(BookImport.id), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)


# Thông tin hóa đơn
class Invoice(db.Model):
    __tablename__ = 'invoice'
    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), default=1)  # bỏ dòng nullable
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    date = Column(Date, nullable=False, default=datetime.today())
    total_price = Column(Float, nullable=False)
    # Chi tiết hóa đơn
    invoice_detail = relationship('InvoiceDetail', backref='invoice', lazy=True)
    # Truy vấn đến bảng lưu thông tin nơi nhận
    shipping = relationship('ShippingDetail', backref='invoice', lazy=True, uselist=False)


# Chi tiết hóa đơn
class InvoiceDetail(db.Model):
    invoice_id = Column(Integer, ForeignKey(Invoice.invoice_id), primary_key=True, nullable=False)
    book_id = Column(Integer, ForeignKey(BookStorage.id), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


# Thông tin đơn hàng được giao
class ShippingDetail(db.Model):
    __tablename__ = 'shipping_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    invoice_id = Column(Integer, ForeignKey(Invoice.invoice_id), nullable=False)
    address = Column(String(100))
    phone = Column(Integer)
    # Trạng thái đơn hàng:
    # > Accepted: ĐH đang được kho xử lý
    # > Delivering: ĐH đang được giao
    # > Completed: ĐH giao hoàn tất
    # > Failed: ĐH có sự cố, hoàn về kho
    status = Column(String(10), default='Accepted')


# Thông tin danh sách yêu thích (wishlist)
class WishDetail(db.Model):
    wish_id = Column(Integer, ForeignKey(Customer.id), primary_key=True, nullable=False)
    book_id = Column(Integer, ForeignKey(BookStorage.id), primary_key=True, nullable=False)


# Bảng quy tắc nghiệp vụ của Quản lý
class SystemRule(db.Model):
    rule_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    # Tên nghiệp vụ > sử dụng trong main.py
    rule = Column(String(20), nullable=False)
    # Giá trị tham chiếu
    value = Column(Integer, nullable=False)
    # Mô tả
    description = Column(String(255))
    # Ví dụ rule = max_debt, value = 20000 có nghĩa là hạn mức nợ của khách không được quá 20k để mua sách


if __name__ == '__main__':
    db.create_all()
