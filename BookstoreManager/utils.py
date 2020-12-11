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
    user = SystemUser(name=name, username=username,
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


class TaskRules:
    pass


# |==============================|
# | TIỆN ÍCH DÙNG CHO KHÁCH HÀNG |
# |==============================|


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


# Test tạo 3 bảng song song độc lập (1 : 2)
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
    w = WishDetail.query.filter(WishDetail.book_id == book_id and WishDetail.wish_id == session['user'].id).first()
    try:
        db.session.delete(w)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)

    return False


# |------------------|
# | Xử lý my account |
# |------------------|


# Sửa thông tin khách hàng  - chưa xong
def change_info(user_id, name, phone, email, address):
    user = Customer.query.filter(Customer.id == user_id).first()
    return user_id


# View lịch sử hóa đơn của khách hàng
def read_my_invoice():
    return Invoice.query.filter(Invoice.customer_id == session["user"]["id"])

# isouter=True : Kết trái


def read_join():
    WishDetail.query.filter(WishDetail.wish_id == session['user'].id)

    # Có nhiêu lấy hết, trùng dữ liệu: theo wishdetail
    # return db.session.query(BookStorage).join(WishDetail)

    # return db.session.query(BookStorage).join(WishDetail).filter(WishDetail.wish_id == current_user.id)

    # return db.session.query(WishDetail, WishDetail.wish_id == current_user.id).join(BookStorage.wish_id)

    # return WishDetail.query.filter(WishDetail.wish_id == current_user.id)

    return db.session.query(BookStorage).join(WishDetail).filter(Invoice.customer_id == session['user'].id).all()


def object_to_dict(obj, found=None):
    if found is None:
        found = set()
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]
    get_key_value = lambda c: (c, getattr(obj, c).isoformat()) if isinstance(getattr(obj, c), datetime) else (c, getattr(obj, c))
    out = dict(map(get_key_value, columns))
    for name, relation in mapper.relationships.items():
        if relation not in found:
            found.add(relation)
            related_obj = getattr(obj, name)
            if related_obj is not None:
                if relation.uselist:
                    out[name] = [object_to_dict(child, found) for child in related_obj]
                else:
                    out[name] = object_to_dict(related_obj, found)
    return out
