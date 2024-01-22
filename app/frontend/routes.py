from app.frontend import frontendBP
from flask import render_template


@frontendBP.route("/auth/login", methods=["GET"], strict_slashes=False)
def login():
    return render_template("auth/login.html")


@frontendBP.route("/auth/register", methods=["GET"], strict_slashes=False)
def register():
    return render_template("auth/registration.html")


@frontendBP.route("/", methods=["GET"], strict_slashes=False)
def index():
    return render_template("tasks/index.html")
