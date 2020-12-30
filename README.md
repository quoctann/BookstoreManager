# Bookstore Management Application

This is the exercise of Software Technology subject, built on Python Flask, MySQL and Bootstrap 4. This app still very primeval so it's just for reference only.



## How to use

We're using PyCharm IDE and Python v3.9 but you'll be free to use any code editor you want. First, you need to create a virtual enviroment and install all package on `requirements.txt`

    pip install -r requirements.txt

The folder `/BookstoreManager` is a Python package so keep it on the same level of your `/venv` which you recently created.

Then you need configure your own MySQL database on `__init__.py` including username, password, schema and also SMTP mail server for recovery email sending service too, you can import our sample database on `/BookstoreManager/BookstoreManager/data/webdb.sql` or run `models.py` to create blank database (we used SQLAlchemy to do that).

That all we done, just run `main.py` and click on address which displaying on your Python console to access this webapp (it's maybe look like this: 127.0.0.0:8000), add */admin* on the URL to access administrator page. If you're using our sample database just login by this admin account:
+ username: quanly
+ password: 123

Or create your own by MySQL Workbench, on table Employee with password was hashing by MD5.

***

Hope this repository is helpful for you :smile:

Happy coding :fire:
