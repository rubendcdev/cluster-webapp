# app/controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models.user import User
from app.services.auth_service import register_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect("/")
    return render_template("login.html")

@auth.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        register_user(
            request.form["username"],
            request.form["email"],
            request.form["password"]
        )
        return redirect("/login")
    return render_template("register.html")

@auth.route("/logout")
def logout():
    logout_user()
    return redirect("/")
