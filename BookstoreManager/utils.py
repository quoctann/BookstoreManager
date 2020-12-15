from flask import session
from flask_login import current_user
from sqlalchemy.orm import class_mapper

from BookstoreManager import app, db
from BookstoreManager.models import *
import hashlib


# |=========================|
# | TIỆN ÍCH DÙNG CHO ADMIN |
# |=========================|


# Tiện ích thêm nhân viên vào hệ thống (Admin)
def add_employee(name, username, password):
    user = Employee(name=name, username=username,
                      password=str(hashlib.md5(password.strip().encode("utf-8")).hexdigest()))
    db.session.add(user)
    db.session.commit()
    return user


# Tiện ích đặt lại các session khi cần thiết
def reset_value():
    session['valid_debt'] = 'init'
    # Session lưu thuộc tính nhân viên đã kiểm tra nợ của KH chưa
    session['debt_checking_status'] = 'init'
    # Lưu tạm thời tên của khách hàng
    session['sell_for'] = 'init'
    if 'import_book' in session:
        del session['import_book']

class TaskRules:
    pass

##########################################################
# Nếu là sách mới, chưa có trong kho, thì cập nhập dữ liệu sách mới vào kho
def import_book(name, quantity, author, category, price):
    book = BookStorage(name=name, instock=quantity, author=author, category=category, selling_price=price)
    try:
        db.session.add(book)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


# Kiểm tra id để bổ sung sách mới
def check_book(book_id):
    book = get_book_by_id(book_id)
    if not book:
        return True
    else:
        return False


# Lấy tổng số lượng và tổng hóa đơn phiếu nhập
def import_stats(import_book):
    total_quantity, total_amount = 0, 0
    if import_book:
        for b in import_book.values():
            total_quantity = total_quantity + b["quantity"]
            total_amount = total_amount + b["quantity"] * b["price"]

    return total_quantity, total_amount



# Tạo 3 bảng song song độc lập (1 : 2)
def add_import(import_book):
    if import_book and current_user.is_authenticated:
        total_quantity, total_amount = import_stats(import_book)
        bookImport = BookImport(employee_incharge=current_user.id, total_cost=total_amount)
        db.session.add(bookImport)

        for b in list(import_book.values()):
            if not get_book_by_id(int(b["id"])):
                book = BookStorage(name=b["name"], instock=b["quantity"], author=b["author"], category=b["category"], selling_price=(b["price"] + b["price"] * 0.1))
                db.session.add(book)
                detail = ImportDetail(book_import=bookImport, book_id=int(b["id"]), quantity=b["quantity"], cost=b["price"])
            else:
                detail = ImportDetail(book_import=bookImport, book_id=int(b["id"]), quantity=b["quantity"], cost=b["price"])
                increase_instock(int(b["id"]), b["quantity"])
            db.session.add(detail)

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
    return False


# Kiểm tra instock trước khi nhập
def check_instock(book_id):
    return BookStorage.query.get(book_id)


# Cập nhập instock mới được bổ sung khi nhập
# Giảm instock của sách trong kho
def increase_instock(book_id, quantity):
    book = BookStorage.query.get(book_id)
    book.instock += quantity
    db.session.add(book)
    db.session.commit()

#########################################################


# |==============================|      ##################################################################################################################
# | TIỆN ÍCH DÙNG CHO KHÁCH HÀNG |      ##################################################################################################################
# |==============================|      ##################################################################################################################


# Thêm khách hàng vào db
def add_customer(name, email, username, password, avatar_path, phone, address):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Customer(username=username, password=password, avatar=avatar_path, name=name,
                 email=email, address=address, phone=phone)
    try:
        db.session.add(u)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


# Kiểm tra đăng nhập của khách hàng
def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return Customer.query.filter(Customer.username == username,
                                 Customer.password == password).first()


# Kiểm tra khách hàng có tồn tại trong db không
def check_customer(username):
    return Customer.query.filter(Customer.username == username).first()


# Kiểm tra email đăng ký của khách có trong db không
def check_mail(email):
    return Customer.query.filter(Customer.email == email).first()


# Chức năng lọc dự liệu bằng kw (keyword) - thanh tìm kiếm trên menu
def search_by_kw(kw=None):
    books = BookStorage.query
    if kw:

        books = books.filter(BookStorage.category.contains(kw)).all()
        if books:
            return books
        else:
            books = BookStorage.query.filter(BookStorage.name.contains(kw))
            if books:
                return books

        # return BookStorage.query.filter(BookStorage.author.contains(kw))


# Lấy tất cả sách có trong db
def get_book_by_name(name=None):
    book = BookStorage.query
    if name:
        book = book.filter(BookStorage.name.contains(name))
    return book.first()


# Chức năng lọc dữ liệu - book-list
def read_books(cate_id=None, kw=None, from_price=None, to_price=None, author=None):
    books = BookStorage.query

    if author:
        books = books.filter(BookStorage.author.contains(author))

    if cate_id:
        books = books.filter(BookStorage.category.contains(cate_id))

    if kw:
        books = books.filter(BookStorage.name.contains(kw))

    if from_price and to_price:
        books = books.filter(BookStorage.selling_price.__gt__(from_price), BookStorage.selling_price.__lt__(to_price))

    return books.all()


# Chức năng xem thông tin sách chi tiết - book-detail
def get_book_by_id(book_id):
    return BookStorage.query.get(book_id)


def get_book_by_cate(cate_id):
    return BookStorage.query.filter(BookStorage.category.contains(cate_id)).all()


# |-------------------|
# | Tiện ích giỏ hàng |
# |-------------------|

def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for b in cart.values():
            total_quantity = total_quantity + b["quantity"]
            total_amount = total_amount + b["quantity"] * b["price"]  # được trỏ từ "price" ở main.py

    return total_quantity, total_amount


# |------------------|
# | Xử lý thanh toán |
# |------------------|

# Giảm instock của sách trong kho
def subtract_instock(book_id, quantity):
    book = BookStorage.query.get(book_id)
    book.instock -= quantity
    db.session.add(book)
    db.session.commit()


# Tạo 3 bảng song song độc lập (1 : 2)
def add_invoice(cart):
    # if cart and current_user.is_authenticated:
    if cart and session.get("user"):
        total_quantity, total_amount = cart_stats(cart)
        invoice = Invoice(customer_id=session['user']['id'], total_price=total_amount)
        db.session.add(invoice)

        for b in list(cart.values()):
            detail = InvoiceDetail(invoice=invoice,
                                   book_id=int(b["id"]),
                                   quantity=b["quantity"],
                                   price=b["price"])
            subtract_instock(int(b["id"]), b["quantity"])
            db.session.add(detail)

        try:
            db.session.commit()
            return True
        except Exception as ex:
            print(ex)
    return False


# Tạo bảng đặt hàng
def add_shipping(invoice_id, name, phone, address):
    shipping = ShippingDetail(invoice_id=invoice_id, name=name, phone=phone, address=address)
    try:
        db.session.add(shipping)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


# |----------------------------------------|
# | Xử lý thêm sách vào danh mục yêu thích |
# |----------------------------------------|


def add_wishlist(wishlist):
    # if wishlist and current_user.is_authenticated:
    if wishlist and session.get("user"):
        # Thêm các sách mới được yêu thích xuống db
        book = None
        for b in list(wishlist.values()):
            book = WishDetail(wish_id=session['user']['id'],
                              book_id=b["id"])
        db.session.add(book)

    try:
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)

    return False


# Kết theo bảng bên trái
# Đọc dữ liệu lấy thông tin sách mà khách hàng đã yêu thích
def read_wish():
    return db.session.query(BookStorage).join(WishDetail).filter(WishDetail.wish_id == session['user']['id']).all()


# Lấy dữ liệu sách theo book_id trong wishlist
def get_wish(book_id):
    return WishDetail.query.filter(book_id == WishDetail.book_id).first()


# Xóa sách ra khỏi danh sách yêu thích - có cập nhập xuống db
def del_wish(book_id):
    w = WishDetail.query.filter(WishDetail.book_id == book_id and WishDetail.wish_id == session['user']['id']).first()
    try:
        db.session.delete(w)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)

    return False



# |--------------------------------------------------|
# | Xử lý chức năng tự thay đổi thông tin khách hàng |
# |--------------------------------------------------|

#   Thay đổi thông tin của khách hàng
def change_info(name, phone, email, address, avatar_path=None):
    user = Customer.query.get(session['user']['id'])
    user.name = name
    user.phone = phone
    user.email = email
    user.address = address
    if avatar_path:
        user.avatar = avatar_path
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


#   thay đổi password
def change_password(new_password):
    new_password = str(hashlib.md5(new_password.strip().encode('utf-8')).hexdigest())
    user = Customer.query.get(session['user']['id'])
    user.password = new_password
    try:
        db.session.add(user)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


# |-------------------------------|
# | Xem lịch sử hóa đơn thanh tóa |
# |-------------------------------|


#   Xem lịch sử hóa đơn của khách hàng: khách hàng có thể có nhiều hóa đơn
#   có session['user']['id'] trong Invoice        : danh sách hóa đơn đã thanh toán của người dùng hiện thời
def read_my_invoice():
    return Invoice.query.filter(Invoice.customer_id == session['user']['id']).all()


#   Lấy id của hóa đơn
#   từ ds hóa đơn của người dùng - xem chi tiết từng hóa đơn 1:  Lấy tổng tiền
def get_invoice_by_id(invoice_id):
    return Invoice.query.filter(Invoice.invoice_id == invoice_id).first()


#   Từ hóa đơn truy vấn để xem thông tin sách đã mua
#   Từ book_id có trong ds InvoiceDetail đã lọc, kết bảng để lấy thông tin sách đã mua
def read_invoice_get_info_book(invoice_id):
    return db.session.query(BookStorage.name, InvoiceDetail.price, InvoiceDetail.quantity).join(InvoiceDetail).\
                            filter(InvoiceDetail.invoice_id == invoice_id).all()


#
def invoice_info(invoice_id):
    total_quantity, total_price = 0, 0
    info = read_invoice_get_info_book(invoice_id)
    id = invoice_id
    for b in info:
        total_quantity = total_quantity + b.quantity
        total_price = total_price + b.quantity * b.price

    return total_quantity, total_price, id
