from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.stay_application_service import list_applications
from app.services.auth_service import update_user, delete_user, register_user
from app.models.user import User

super_admin = Blueprint("super_admin", __name__)

@super_admin.route("/super-admin/solicitudes")
@login_required
def dashboard():
    if current_user.role != "super_admin":
        flash("Acceso denegado. Se requiere cuenta de Super Admin.", "error")
        return redirect(url_for("public.index"))
    
    solicitudes = list_applications()
    return render_template("super_admin/dashboard.html", solicitudes=solicitudes)

@super_admin.route("/super-admin/administradores")
@login_required
def administradores():
    if current_user.role != "super_admin":
        flash("Acceso denegado.", "error")
        return redirect(url_for("public.index"))

    admins = User.query.filter_by(role="admin").all()
    return render_template("super_admin/administradores.html", admins=admins)


@super_admin.route("/super-admin/administradores/crear", methods=["POST"])
@login_required
def crear_admin():
    if current_user.role != "super_admin":
        flash("Acceso denegado.", "error")
        return redirect(url_for("public.index"))

    register_user(
        nombre=request.form.get("nombre"),
        apellido_paterno=request.form.get("apellido_paterno"),
        apellido_materno=request.form.get("apellido_materno"),
        correo=request.form.get("correo"),
        telefono=request.form.get("telefono"),
        password=request.form.get("password"),
        role="admin"
    )

    flash("Administrador creado correctamente.", "success")
    return redirect(url_for("super_admin.administradores"))


@super_admin.route("/super-admin/administradores/<int:user_id>/eliminar", methods=["POST"])
@login_required
def eliminar_admin(user_id):
    if current_user.role != "super_admin":
        flash("Acceso denegado.", "error")
        return redirect(url_for("public.index"))
    if user_id == current_user.id:
        flash("No puedes eliminar tu propia cuenta.", "error")
        return redirect(url_for("super_admin.administradores"))


    delete_user(user_id)
    flash("Administrador eliminado correctamente.", "success")
    return redirect(url_for("super_admin.administradores"))

@super_admin.route("/super-admin/administradores/<int:user_id>/editar", methods=["POST"])
@login_required
def editar_admin(user_id):
    if current_user.role != "super_admin":
        flash("Acceso denegado.", "error")
        return redirect(url_for("public.index"))

    update_user(
        user_id=user_id,
        nombre=request.form.get("nombre"),
        apellido_paterno=request.form.get("apellido_paterno"),
        apellido_materno=request.form.get("apellido_materno"),
        correo=request.form.get("correo"),
        telefono=request.form.get("telefono"),
        password=request.form.get("password"),  # solo se actualiza si viene algo
        role="admin"
    )

    flash("Administrador actualizado correctamente.", "success")
    return redirect(url_for("super_admin.administradores"))