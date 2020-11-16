from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from BookstoreManager import admin, db


class SellingBookView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/selling-book.html')


admin.add_view(SellingBookView(name='Bán sách'))
