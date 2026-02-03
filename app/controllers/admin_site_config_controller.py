# app/controllers/admin_site_config_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.site_config_service import get_config, set_config

admin_site_config = Blueprint("admin_site_config", __name__)

@admin_site_config.route("/admin/site-config", methods=["GET", "POST"])
@login_required
def edit_site_config():
    # Verificar que el usuario es admin
    if not current_user.is_authenticated or current_user.role != "admin":
        flash("Acceso denegado", "danger")
        return redirect(url_for("public.index"))
    
    if request.method == "POST":
        texto_estancias = request.form.get("texto_estancias", "")
        set_config("texto_estancias", texto_estancias)
        flash("Configuración actualizada correctamente", "success")
        return redirect(url_for("admin_site_config.edit_site_config"))
    
    # Obtener el texto actual
    texto_estancias = get_config("texto_estancias", "")
    
    return render_template("admin/site_config_edit.html", texto_estancias=texto_estancias)
