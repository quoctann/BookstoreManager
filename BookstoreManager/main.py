from BookstoreManager import app, login, utils
from BookstoreManager.admin import *
from BookstoreManager.models import *
from flask import render_template, request, redirect, session, url_for
from flask_login import login_user
import hashlib


# Điều hướng tới trang chủ mặc định
@app.route("/")
def index():
    return render_template("index.html")


# Xử lý action login
@app.route("/login-admin", methods=["GET", "POST"])
# Phương thức này được gọi từ login.html
def login_admin():
    # Chỉ xử lý đăng nhập khi sử dụng phương thức POST
    if request.method == "POST":
        # Lấy dữ liệu từ form (thông qua request)
        username = request.form.get("loginUsername")
        password = request.form.get("loginPassword")
        # Dùng thuật toán MD5 băm mã ra dưới dạng hexa
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        # Strip() dùng để bỏ khoảng trắng ở hai đầu chuỗi ký tự
        user = SystemUser.query.filter(SystemUser.username == username.strip(),
                                       SystemUser.password == password).first()
        # Nếu không giá trị thì trả về null
        if user:
            login_user(user=user)
    # Thực tế là chuyển đến trang admin -> index.html
    return redirect("/admin")


# Xử lý action register
@app.route("/register/", defaults={'err_msg': None}, methods=["GET", "POST"])
@app.route("/register/<err_msg>", methods=["GET", "POST"])
# Phương thức này được gọi từ login.html
def register_admin(err_msg):
    # Chỉ xử lý đăng nhập khi sử dụng phương thức POST
    if not err_msg:
        # Nếu không có lỗi
        if request.method == "POST":
            # Lấy dữ liệu từ form (thông qua request)
            username = request.form.get("registerUsername")
            name = request.form.get("registerName")
            password = request.form.get("registerPassword")
            confirm = request.form.get("confirmPassword")
            # Nếu mật khẩu nhập lại không đúng
            if confirm.strip() != password.strip():
                # Lưu một giá trị tạm báo lỗi trong session
                session["message"] = "Mật khẩu không khớp"
            else:
                # Tiện ích thêm người dùng vào hệ thống
                if utils.add_admin(name=name, username=username, password=password):
                    session["message"] = "Đăng ký thành công"
                else:
                    session["message"] = "Server internal error"
        if session["message"]:
            return redirect(url_for("login_admin", err_msg=session["message"]))
        else:
            return redirect(url_for("login_admin", err_msg=session["message"]))
    # Nếu có lỗi từ đầu
    else:
        return render_template('register.html')

# Khi đăng nhập mặc định chỉ lưu ID, nhưng khi muốn truy xuất
# dữ liệu của đối tượng thì hàm này sẽ được gọi để tham chiếu
# đến đối tượng đang đăng nhập
@login.user_loader
def user_load(user_id):
    return SystemUser.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
