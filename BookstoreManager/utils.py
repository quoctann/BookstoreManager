from flask_login import current_user

from BookstoreManager import app, db
from BookstoreManager.models import SystemUser, Customer, BookStorage, Invoice, InvoiceDetail, WishDetail, \
    ShippingDetail
import hashlib


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


def check_login(username, password):
    password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    return Customer.query.filter(Customer.username == username,
                                 Customer.password == password).first()


def check_Customer(username):
    return Customer.query.filter(Customer.username == username).first()


def check_mail(email):
    return Customer.query.filter(Customer.email == email).first()


# Chức năng lọc dữ liệu theo 1 từ khóa - bar-footer
# chức năng này cần kết bảng, và tạo thêm bảng BookCate
def read_books(kw=None):
    books = BookStorage.query
    if kw:
        books = books.filter(BookStorage.name.contains(kw))

    return books.all()


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
    return BookStorage.query.filter(BookStorage.category == cate_id).all()


#   ----------------------    Phần xử lý chức năng giỏ hàng -------------------

def cart_stats(cart):
    total_quantity, total_amount = 0, 0
    if cart:
        for b in cart.values():
            total_quantity = total_quantity + b["quantity"]
            total_amount = total_amount + b["quantity"] * b["price"]  # được trỏ từ "price" ở main.py

    return total_quantity, total_amount


#   ----------------------- Xử lý thanh toán ----------------------


# test tạo 3 bảng song song độc lập (1 : 2)
def add_invoice(cart):
    if cart and current_user.is_authenticated:
        total_quantity, total_amount = cart_stats(cart)
        invoice = Invoice(customer_id=current_user.id, total_price=total_amount)
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


# ---------------------- xử lý thêm sách vào danh mục yêu thích -----------------------
def add_wishlist(wishlist):
    if wishlist and current_user.is_authenticated:
        # thêm các sách mới được yêu thích xuống db
        for b in list(wishlist.values()):
            book = WishDetail(wish_id=current_user.id,
                              book_id=b["id"])
        db.session.add(book)

    try:
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)

    return False


# kết theo bảng bên trái
# Đọc dữ liệu lấy thông tin sách mà khách hàng đã yêu thích
def read_wish():
    return db.session.query(BookStorage).join(WishDetail).filter(WishDetail.wish_id == current_user.id).all()


# Lấy dữ liệu sách theo book_id trong wishlist
def get_wish(book_id):
    return WishDetail.query.filter(book_id  == WishDetail.book_id).first()


# Xóa sách ra khỏi danh sách yêu thích - có cập nhập xuống db
def del_wish(book_id):
    w = WishDetail.query.filter(WishDetail.book_id == book_id and WishDetail.wish_id == current_user.id).first()
    try:
        db.session.delete(w)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)

    return False


# --------------    my-acc    -------------

# sửa thông tin khách hàng  - chưa xong
def change_info(user_id, name, phone, email, address):
    user = Customer.query.filter(Customer.id == user_id).first()
    return user_id


# view lịch sử hóa đơn của khách hàng
def read_my_invoice():
    return Invoice.query.filter(Invoice.customer_id == current_user.id)



# isouter=True : Kết trái

def read_join():
    WishDetail.query.filter(WishDetail.wish_id == current_user.id)

    # Có nhiêu lấy hết, trùng dữ liệu: theo wishdetail
    # return db.session.query(BookStorage).join(WishDetail)

    # return db.session.query(BookStorage).join(WishDetail).filter(WishDetail.wish_id == current_user.id)

    # return db.session.query(WishDetail, WishDetail.wish_id == current_user.id).join(BookStorage.wish_id)

    # return WishDetail.query.filter(WishDetail.wish_id == current_user.id)

    return db.session.query(BookStorage).join(WishDetail).filter(Invoice.customer_id == current_user.id).all()

