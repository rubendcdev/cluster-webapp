# app/controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.services.auth_service import register_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        if not correo or not password:
            flash("Correo y contraseña son obligatorios.", "error")
            return render_template("login.html"), 400

        user = User.query.filter_by(correo=correo).first()
        if not user or not check_password_hash(user.password, password):
            flash("Credenciales inválidas.", "error")
            return render_template("login.html"), 401

        login_user(user, remember=remember)
        next_url = request.args.get("next") or url_for("public.index")
        return redirect(next_url)
    return render_template("login.html", mode="login")

@auth.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido_paterno = request.form.get("apellido_paterno", "").strip()
        apellido_materno = request.form.get("apellido_materno", "").strip()
        telefono = request.form.get("telefono", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not nombre or not apellido_paterno or not correo or not password or not confirm:
            flash("Nombre, apellido paterno, correo y contraseña son obligatorios.", "error")
            return render_template("login.html", mode="register"), 400

        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "error")
            return render_template("login.html", mode="register"), 400

        if len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "error")
            return render_template("login.html", mode="register"), 400

        if password != confirm:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("login.html", mode="register"), 400

        if User.query.filter_by(correo=correo).first():
            flash("El correo ya está registrado.", "error")
            return render_template("login.html", mode="register"), 409

        try:
            register_user(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                correo=correo,
                telefono=telefono,
                password=password,
            )
        except IntegrityError:
            flash("El correo ya existe.", "error")
            return render_template("login.html", mode="register"), 409

        flash("Registro exitoso. Inicia sesión.", "success")
        return redirect(url_for("auth.login"))
    return render_template("login.html", mode="register")

@auth.route("/logout")
def logout():
    logout_user()
    flash("Has salido de tu sesión.", "success")
    return redirect(url_for("public.index"))
