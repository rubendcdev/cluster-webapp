from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.stay_application_service import list_applications

super_admin = Blueprint("super_admin", __name__)

@super_admin.route("/super-admin/solicitudes")
@login_required
def dashboard():
    if current_user.role != "super_admin":
        flash("Acceso denegado. Se requiere cuenta de Super Admin.", "error")
        return redirect(url_for("public.index"))
    
    solicitudes = list_applications()
    return render_template("super_admin/dashboard.html", solicitudes=solicitudes)
