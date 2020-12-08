from flask import render_template, request, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message, Mail
from BookstoreManager import app, login, utils, mail, decorator
from BookstoreManager.admin import *
from BookstoreManager.models import *
import hashlib, os, json
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

randomToken = URLSafeTimedSerializer('this_is_a_secret_key')


# Xử lý action login-Customer
@app.route('/login', methods=["get", "post"])
def login_customer():
    err_msg = ""
    if request.method == 'POST':
        # lấy thông tin đăng nhập
        username = request.form.get('username')
        password = request.form.get('password', '')

        # kiểm tra đăng nhập
        customer = utils.check_login(username=username, password=password)
        if customer:
            login_user(user=customer)
            if "next" in request.args:
                return redirect(request.args["next"])

            return redirect(url_for('index'))
        else:
            err_msg = "Thiếu thông tin hoặc sai mật khẩu"

    return render_template("login.html", err_msg=err_msg)


@app.route("/logout")
def logout():
    logout_user()
    # Xóa hết các bộ nhớ tạm của session
    if 'cart' in session:
        del session['cart']
    if 'wish' in session:
        del session['wish']
    return redirect(url_for("index"))


# Xử lý action register-Customer
@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ""
    # Chỉ xử lý đăng nhập khi sử dụng phương thức POST
    if request.method == 'POST':
        # Đối chiếu password và confirm từ form (thông qua request)
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        if confirm.strip() == password.strip():
            # Tiếp tục lấy dữ liệu từ form (thông qua request)
            name = request.form.get('name')
            email = request.form.get('email')
            username = request.form.get('username')
            phone = request.form.get('phone')
            address = request.form.get('address')

            avatar = request.files["avatar"]
            avatar_path = 'images/upload/%s' % avatar.filename
            avatar.save(os.path.join(app.root_path,
                                     'static/',
                                     avatar_path))
            if utils.add_customer(username=username, password=password, avatar_path=avatar_path, name=name,
                                  email=email, address=address, phone=phone):
                return redirect('/')
            else:
                err_msg = "Hệ thống đang có lỗi! Vui lòng quay lại sau!"
        else:
            err_msg = "Mật khẩu KHÔNG khớp!"

    return render_template('register.html', err_msg=err_msg)


# Xử lý action ForgotPassword-Customer
@app.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    err_msg = ""
    if request.method == 'POST':
        try:
            email = request.form.get("email")
            if utils.check_mail(email=email):
                return redirect(url_for("request_sent", user_email=email))
            else:
                err_msg = "Nhập sai email"
        except IntegrityError:
            err_msg = "Nhập sai email"

    return render_template("forgot-password.html", err_msg=err_msg)


@app.route('/email-verification/<user_email>', methods=["GET", "POST"])
def email_verify(user_email):
    token = randomToken.dumps(user_email, salt="email_confirm")
    msg = Message('Thư xác nhận', sender='emailverifywebapp@gmail.com', recipients=[user_email])
    link = url_for('confirm_email', token=token, _external=True)
    msg.body = 'Vui lòng nhấn vào liên kết sau để xác nhận email. Liên kết của bạn là: {}'.format(link)
    mail.send(msg)
    return render_template("verify-email.html", user_email=user_email, )


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = randomToken.loads(token, salt='email_confirm', max_age=900)
    except SignatureExpired:
        return render_template('verify-expired.html')
    return render_template('verify-success.html', email=email)


@app.route('/request_sent/<user_email>', methods=["GET", "POST"])
def request_sent(user_email):
    token = randomToken.dumps(user_email, salt="recovery_account")
    msg = Message('Khôi phục tài khoản', sender='emailverifywebapp@gmail.com', recipients=[user_email])
    link = url_for('recovery_account', token=token, user_email=user_email, _external=True)
    msg.body = 'Bạn đang tiến hành đặt lại mật khẩu, liên kết sẽ hết hạn sau 15 phút. Nhấn vào liên kết sau ' \
               'để đặt lại mật khẩu: {}'.format(link)
    mail.send(msg)
    return render_template("recovery-sent.html", user_email=user_email)


@app.route('/recovery_account/<token>/<user_email>', methods=['GET', 'POST'])
def recovery_account(token, user_email):
    try:
        e = randomToken.loads(token, salt='recovery_account', max_age=3600)
    except SignatureExpired:
        return render_template('verify-expired.html')
    if request.method == 'POST':
        password = request.form.get("password")
        user = utils.check_mail(user_email)
        if user:
            user.password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
            db.session.add(user)
            db.session.commit()
            return render_template('password-reset.html')
    return render_template('recovery-account.html')


# Khi đăng nhập mặc định chỉ lưu ID, nhưng khi muốn truy xuất
# dữ liệu của đối tượng thì hàm này sẽ được gọi để tham chiếu
# đến đối tượng đang đăng nhập
@login.user_loader
def user_load(user_id):
    return Customer.query.get(user_id)


# Điều hướng tới trang chủ mặc định
@app.route('/')
def index():
    booknew = BookStorage.query.filter(BookStorage.instock > 0).limit(10).all()
    book_tieuthuyet = BookStorage.query.filter(BookStorage.category.startswith("Tieu Thuyet")).limit(10).all()
    return render_template('index.html', booknew=booknew, book_tieuthuyet=book_tieuthuyet)


# Xem các thể loại sách
@app.route('/book-list')
def book_list(cate_id=None):
    author = request.args.get('author')
    cate_id = request.args.get('category_id')
    kw = request.args.get('kw')
    from_price = request.args.get('from_price')
    to_price = request.args.get('to_price')
    books = utils.read_books(cate_id=cate_id, kw=kw, from_price=from_price, to_price=to_price, author=author)

    return render_template('book-list.html', books=books, cate_id=cate_id)


# list sách theo category đường dẫn
@app.route('/book-list/<cate_id>')
def book_list_by_cate(cate_id):
    books = utils.get_book_by_cate(cate_id)
    return render_template('book-list.html', books=books, cate_id=cate_id)


# Xem thông tin sách cụ thể
@app.route('/book-detail/<int:book_id>')
def book_detail(book_id):
    book = utils.get_book_by_id(book_id=book_id)
    book_relate = BookStorage.query.filter(BookStorage.category == book.category).limit(10).all()

    return render_template('book-detail.html', book=book, book_relate=book_relate)


# --------------------- Phần xử lý chức năng giỏ hàng -----------------------------
# xử lý theo main.js    addToCart()
@app.route('/api/cart', methods=['post'])
def add_to_cart():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Bạn cần đăng nhập để sử dụng tính năng này!'})

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = json.loads(request.data)

    id = str(data.get("id"))
    name = data.get("name")
    price = data.get("selling_price")  # từ khóa "selling_price" chỉ qua main.js
    path = data.get("path")

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,  # từ khóa "price" trỏ tới utils
            "path": path,
            "quantity": 1
        }

    session['cart'] = cart

    quan, price = utils.cart_stats(cart)

    return jsonify({
        "total_amount": price,
        "total_quantity": quan,
        'message': 'Sách đã được thêm vào giỏ!'  # không bật alert nên không hiển thị thông báo này
    })


@app.route('/api/subtractcart', methods=['post'])
def subtract_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = json.loads(request.data)

    id = str(data.get("id"))

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] - 1
    session['cart'] = cart

    quan, price = utils.cart_stats(cart)

    return jsonify({
        "total_amount": price,
        "total_quantity": quan
    })


@app.route('/api/deletecart', methods=['post'])
def delete_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = json.loads(request.data)

    id = str(data.get("id"))

    if id in cart:
        cart.pop(id)
    session['cart'] = cart

    if not cart:
        del session['cart']

    quan, price = utils.cart_stats(cart)

    return jsonify({
        "total_amount": price,
        "total_quantity": quan
    })


@app.route('/api/buy', methods=['post'])
def buy_now():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Bạn cần đăng nhập để sử dụng tính năng này!'})

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = json.loads(request.data)

    id = str(data.get("id"))
    name = data.get("name")
    price = data.get("selling_price")  # từ khóa "selling_price" chỉ qua main.js
    path = data.get("path")

    if id in cart:
        cart[id]["quantity"] = cart[id]["quantity"] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,  # từ khóa "price" trỏ tới utils
            "path": path,
            "quantity": 1
        }

    session['cart'] = cart

    return redirect('/checkout')



# dữ liệu nhận được từ utils thông qua session cart
@app.route('/cart')
@decorator.login_required_cart
def cart():
    quantity, price = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_amount": price,
        "total_quantity": quantity
    }
    return render_template('cart.html', cart_info=cart_info)


# -------------------------- Xử lý thanh toán -------------------------------------

# Xử lý thanh toán, ghi thông tin người nhận hàng, địa chỉ nhận
@app.route('/checkout', methods=['get', 'post'])
@login_required
def checkout():
    err_msg = ""
    quantity, price = utils.cart_stats(session.get('cart'))
    cart_info = {
        "total_amount": price,
        "total_quantity": quantity
    }
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        if phone and address and name:
            if 'cart' in session:
                utils.add_invoice(session.get('cart'))
                utils.add_shipping(invoice_id=current_user.id, name=name, phone=phone, address=address)

                del session['cart']
                err_msg = "Bạn đã thanh toán thành công!"
                redirect('login?next=/checkout')
            else:
                err_msg = "Không có sách để thanh toán!"
        else:
            err_msg = "Bạn phải điền thông tin!"

    return render_template('checkout.html', cart_info=cart_info, err_msg=err_msg)


# ----------------------- Danh sách yêu thích , chưa kết được bản   ---------------------------

# Đăng nhập thành công mới có thể thêm sách vào wishlist, chưa đăng nhập hiện thông báo
@app.route('/api/wish', methods=['post'])
def add_to_wish():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Bạn cần đăng nhập để sử dụng tính năng này!'})

    if 'wish' not in session:
        session['wish'] = {}

    wish = session['wish']

    data = json.loads(request.data)

    id = str(data.get("id"))
    name = data.get("name")
    price = data.get("selling_price")
    path = data.get("path")

    # nếu book_id mới thêm vào có trong ds, thì xóa bỏ
    if id in wish:
        return jsonify({'message': 'Đã có trong danh sách yêu thích'})


    #   Sách yêu thích mới được thêm vào cuối ds
    #   thêm book_id vào trong ds yêu thích của người dùng hiện thời
    else:
        wish[id] = {
            "id": id,
            "name": name,
            "price": price,
            "path": path
        }

    session['wish'] = wish

    if utils.add_wishlist(session.get('wish')):
        return jsonify({'message': 'Sách đã được thêm vào danh mục yêu thích!'})

    return jsonify({'message': 'failed'})


# Xóa sách trong ds yêu thích
@app.route('/api/deletewish', methods=['post'])
def delete_wish():
    if 'wish' not in session:
        session['wish'] = {}

    wish = session['wish']

    data = json.loads(request.data)

    id = str(data.get("id"))

    if id in wish:
        wish.pop(id)
    session['wish'] = wish

    if not wish:
        del session['wish']

    return jsonify({
        'message': 'Sách đã được xóa khỏi danh sách yêu thích!'
    })


# Khi đăng nhập thành công, query xuống db để hiện thị danh sách yêu thích - chưa làm được
@app.route('/wishlist')
@decorator.login_required_wishlist
@login_required
def wishlist():
    return render_template('wishlist.html')


# Chưa xây dựng chức năng
@app.route('/my-account')
@login_required
def my_account():
    return render_template('my-account.html')


if __name__ == "__main__":
    app.run(debug=True)
