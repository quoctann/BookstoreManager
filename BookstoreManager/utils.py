from flask_login import current_user

from BookstoreManager import app, db
from BookstoreManager.models import SystemUser, Customer, BookStorage, Invoice, InvoiceDetail, WishDetail, ShippingDetail
import hashlib


def add_admin(name, username, password):
    user = SystemUser(name=name, username=username,
                      password=str(hashlib.md5(password.strip().encode("utf-8")).hexdigest()))
    db.session.add(user)
    db.session.commit()

    return user


def add_Customer(name, email, username, password, avatar_path):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = Customer(name=name, email=email,
                 username=username, password=password,
                 avatar=avatar_path)
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

# def add_invoice(cart):
#     if cart and current_user.is_authenticated:
#         total_quantity, total_amount = cart_stats(cart)
#         invoice = Invoice(customer_id=current_user.id, total_price=total_amount)
#         db.session.add(invoice)
#
#         for b in list(cart.values()):
#             detail = InvoiceDetail(invoice=invoice,
#                                    book_id=int(b["id"]),
#                                    quantity=b["quantity"],
#                                    price=b["price"])
#             db.session.add(detail)
#
#         try:
#             db.session.commit()
#             return True
#         except Exception as ex:
#             print(ex)
#     return False


def add_invoice(cart, phone, address):
    if cart and current_user.is_authenticated:
        total_quantity, total_amount = cart_stats(cart)
        invoice = Invoice(customer_id=current_user.id, total_price=total_amount)
        db.session.add(invoice)

        shipping = ShippingDetail(invoice=invoice, phone=phone, address=address)
        db.session.add(shipping)

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



# Query db theo current_user để lấy danh sách yêu thích hiển thị cho người dùng hiện thời
# def get_wish_detail_by_current_user(current_user_id):
#     return WishDetail.query.join(WishDetail, Wish.wish_id == WishDetail.wish_id).filer(Wish.customer_id.contains(current_user_id)).add_columns(Wish.wish_id).all()



