from flask import render_template, request
from BookstoreManager import app


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
