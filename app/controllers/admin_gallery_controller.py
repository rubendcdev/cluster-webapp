# app/controllers/admin_gallery_controller.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_gallery = Blueprint("admin_gallery", __name__)

@admin_gallery.route("/admin/gallery")
@login_required
def admin_gallery_view():
    if current_user.role != "admin":
        return "Acceso denegado", 403
    return render_template("admin/gallery_crud.html")
