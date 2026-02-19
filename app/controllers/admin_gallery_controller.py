"""Controlador para la administración de la galería."""

import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.services.gallery_service import get_all_images, create_image, get_image, update_image, delete_image


admin_gallery = Blueprint("admin_gallery", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_gallery.route("/gallery/new", methods=["GET", "POST"])
@login_required
def admin_gallery_new():
    if current_user.role != "admin":
        return "Acceso denegado", 403

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip() or None
        file = request.files.get("image")

        if not title or not file or not file.filename:
            flash("El título y la imagen son obligatorios.", "danger")
        elif not allowed_file(file.filename):
            flash("Formato de imagen no permitido.", "danger")
        else:
            filename = secure_filename(file.filename)
            # evitar colisiones usando timestamp
            import time

            timestamp = str(int(time.time()))
            image_filename = f"{timestamp}_{filename}"

            upload_dir = os.path.join(current_app.static_folder, "uploads", "gallery")
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, image_filename))

            create_image(title=title, description=description, image=image_filename)
            flash("Imagen creada correctamente.", "success")
            return redirect(url_for("public.gallery"))

    return render_template("gallery/new.html")


@admin_gallery.route("/gallery/<int:image_id>/edit", methods=["GET", "POST"])
@login_required
def admin_gallery_edit(image_id):
    if current_user.role != "admin":
        return "Acceso denegado", 403

    image = get_image(image_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip() or None
        file = request.files.get("image")

        if not title:
            flash("El título es obligatorio.", "danger")
            return render_template("gallery/edit.html", image=image)

        image_filename = None
        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Formato de imagen no permitido.", "danger")
                return render_template("gallery/edit.html", image=image)

            # eliminar imagen anterior si existe
            if image.image:
                old_path = os.path.join(current_app.static_folder, "uploads", "gallery", image.image)
                if os.path.exists(old_path):
                    os.remove(old_path)

            filename = secure_filename(file.filename)
            import time

            timestamp = str(int(time.time()))
            image_filename = f"{timestamp}_{filename}"
            upload_dir = os.path.join(current_app.static_folder, "uploads", "gallery")
            os.makedirs(upload_dir, exist_ok=True)
            file.save(os.path.join(upload_dir, image_filename))

        update_image(image_id, title=title, description=description, image_filename=image_filename)
        flash("Imagen actualizada correctamente.", "success")
        return redirect(url_for("public.gallery"))

    return render_template("gallery/edit.html", image=image)


@admin_gallery.route("/gallery/<int:image_id>/delete", methods=["POST"])
@login_required
def admin_gallery_delete(image_id):
    if current_user.role != "admin":
        return "Acceso denegado", 403

    image = get_image(image_id)

    # eliminar archivo físico si existe
    if image.image:
        image_path = os.path.join(current_app.static_folder, "uploads", "gallery", image.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    delete_image(image_id)
    flash("Imagen eliminada correctamente.", "success")
    return redirect(url_for("public.gallery"))
