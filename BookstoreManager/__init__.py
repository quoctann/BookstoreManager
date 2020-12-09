from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
<<<<<<< HEAD
=======
from flask_mail import Mail  

>>>>>>> 974f5fb6b309adcd507256796c115eb5c8433bfe

app = Flask(__name__)
app.secret_key = "y1478whdbh1183132qwchda"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:P@ssw0rd@localhost/webstoredb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app=app)
admin = Admin(app=app, name='Quản trị hệ thống',
              template_mode="bootstrap4")
login = LoginManager(app)
