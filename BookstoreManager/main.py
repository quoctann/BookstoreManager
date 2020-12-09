from BookstoreManager import app, login, utils
from BookstoreManager.admin import *
from BookstoreManager.models import *
from flask import render_template, request, redirect, session, url_for, jsonify
from flask_login import login_user
import hashlib
import json
import os


# |=============|
# | XỬ LÝ CHUNG |
# |=============|


# Điều hướng tới trang chủ mặc định
@app.route("/")
def index():
    utils.reset_value()
    session['test_num'] = 0
    return render_template("index.html")


# Khi đăng nhập mặc định chỉ lưu ID, nhưng khi muốn truy xuất
# dữ liệu của đối tượng thì hàm này sẽ được gọi để tham chiếu
# đến đối tượng đang đăng nhập
@login.user_loader
def user_load(user_id):
    return SystemUser.query.get(user_id)


# |=====================|
# | XỬ LÝ PHÂN HỆ ADMIN |
# |=====================|


# Xử lý action login của admin
@app.route("/login-admin", methods=["GET", "POST"])
# Phương thức này được gọi từ login.html
def login_admin():
    utils.reset_value()
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


# Xử lý action thêm nhân viên
@app.route("/register-employee/", defaults={'err_msg': None}, methods=["GET", "POST"])
@app.route("/register-employee/<err_msg>", methods=["GET", "POST"])
# Phương thức này được gọi từ login.html
def register_employee(err_msg):
    # Chỉ xử lý đăng nhập khi sử dụng phương thức POST
    if not err_msg:
        # Nếu không có lỗi và bút submit được trigger
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
                if utils.add_employee(name=name, username=username, password=password):
                    session["message"] = "Đăng ký thành công"
                else:
                    session["message"] = "Server internal error"
        if session["message"]:
            return redirect(url_for("login_admin", err_msg=session["message"]))
        else:
            return redirect(url_for("login_admin", err_msg=session["message"]))
    # Nếu có lỗi từ đầu
    else:
        return render_template('register-employee.html')


# Xử lý action bán sách
@app.route('/admin/sellview/', methods=["GET", "POST"])
def check_debt():
    # valid_debt lưu trạng thái của tác vụ với các giá trị:
    # init: khởi tạo, bắt đầu bán hàng
    # violated: vi phạm quy định, xuất thông báo lỗi
    # OK: khách hàng hợp lệ, cho phép bán
    if request.method == "POST" and \
            (session['valid_debt'] == 'init' or session['valid_debt'] == 'violated'):
        customer_id = request.form.get('customer_id')
        customer = Customer.query.filter_by(id=customer_id).first()
        # Nếu query khách hàng có tồn tại
        if customer:
            debt = int(customer.debt)
            # Kiểm tra nghiệp vụ
            if debt and debt <= 20000:
                session['valid_debt'] = 'OK'
                session['sell_for'] = customer.name
            else:
                session['valid_debt'] = 'violated'
            return redirect(url_for('sellview.index'))
        # Sau khi bán xong trả lại trạng thái ban đầu
        session['valid_debt'] = 'init'

    # Sau khi đã kiểm tra và khách hàng hợp lệ
    if request.method == "POST" and (session['valid_debt'] == 'OK'):
        # Lấy toàn bộ request từ form > kiểu dictionary
        for arg in request.form:
            # Input name: quantity-số là số lượng sản phẩm tương ứng với input name 'số' mà id sản phẩm
            # request.form sẽ lấy tất cả các request từ form
            # request.form sẽ trả về InmutableDict, parse sang dict bằng to_dict để sử dụng len()
            # arg là trường key của một phần tử dict tương đương với input name
            for count in range(len(request.form.to_dict())):
                if arg == ('quantity-'+str(count)):
                    print('quantity is', request.form.get(arg))
                elif arg == str(count):
                    print('product is', request.form.get(arg))
        print('OK')

    # Gọi phương thức index(self) từ admin.py
    return redirect(url_for('sellview.index'))


# |===================================|
# | APPLICATION PROGRAMMING INTERFACE |
# |===================================|

# Test lấy giá trị
@app.route('/api/get_value', methods=['post'])
def get_value():
    if json.loads(request.data):
        data = json.loads(request.data)
        id = str(data.get("id"))
        return jsonify({
            "message": session['valid_debt'],
        })
    else:
        pass


if __name__ == "__main__":
    app.run(debug=True)
