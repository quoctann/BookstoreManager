from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from BookstoreManager import db


class CommonIdentityBase(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)


class AuthIndentityBase(db.Model):
    __abstract__ = True
    username = Column(String(20), nullable=False)
    password = Column(String(20), nullable=False)


# Thông tin nhân viên và vai trò trong hệ thống
class Employee(CommonIdentityBase, AuthIndentityBase):
    __tablename__ = 'employee'
    role = Column(String(10), nullable=False)
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
    phone = Column(Integer, nullable=False)
    debt = Column(Float, default=0)
    # Đã trả những khoản nợ nào
    paid_debt = relationship('DebtCollection', backref='customer', lazy=True)
    # Có những hóa đơn nào
    paid_invoice = relationship('Invoice', backref='customer', lazy=True)


# Dữ liệu khi nhân viên thu nợ khách hàng
class DebtCollection(db.Model):
    __tablename__ = 'debt_collection'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)


# Thông tin sách trong kho
class BookStorage(CommonIdentityBase):
    __tablename__ = 'book_storage'
    instock = Column(Integer, nullable=False)
    author = Column(String(20), nullable=False)
    category = Column(String(20), nullable=False)
    selling_price = Column(Float, nullable=False)
    # Sách được nhập bởi những đơn hàng nào
    imported_by = relationship('ImportDetail', backref='book_storage', lazy=True)
    # Sách được bán trên những hóa đơn nào
    sold_invoice = relationship('Invoice', backref='book_storage', lazy=True)


class BookImport(db.Model):
    __tablename__ = 'book_import'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    total_cost = Column(Float, nullable=False)
    # Nhân viên chịu trách nhiệm nhập sách
    employee_incharge = Column(Integer, ForeignKey(Employee.id))
    # Chi tiết đơn hàng
    import_detail = relationship('ImportDetail', backref='book_import', lazy=True)


class ImportDetail(db.Model):
    __tablename__ = 'import_detail'
    book_id = Column(Integer, ForeignKey(BookStorage.id), primary_key=True, nullable=False)
    import_id = Column(Integer, ForeignKey(BookImport.id), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)


# Thông tin hóa đơn
class Invoice(db.Model):
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(Integer, ForeignKey(Employee.id), nullable=False)
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    date = Column(Date, nullable=False)
    total_price = Column(Float, nullable=False)
    # Chi tiết hóa đơn
    invoice_detail = relationship('InvoiceDetail', backref='invoice', lazy=True)


# Chi tiết hóa đơn
class InvoiceDetail(db.Model):
    invoice_id = Column(Integer, ForeignKey(Invoice.id), primary_key=True, nullable=False)
    book_id = Column(Integer, ForeignKey(BookStorage.id), primary_key=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)


if __name__ == '__main__':
    db.create_all()
