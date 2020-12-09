from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail  


app = Flask(__name__)
# Configuration of MySQL Server
app.secret_key = "y1478whdbh1183132qwchda"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Abc1234%^&@localhost/webstoredb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# Configuration of Mail Server
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'emailverifywebapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'quoctan123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
db = SQLAlchemy(app=app)
login = LoginManager(app=app)
mail = Mail(app=app)



db = SQLAlchemy(app=app)
admin = Admin(app=app, name='Quản trị hệ thống',
              template_mode="bootstrap4")
login = LoginManager(app)