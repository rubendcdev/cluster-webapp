# app/controllers/admin_success_cases_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from datetime import datetime
from app.services.success_case_service import create_case, list_cases, delete_case, get_case, update_case
from werkzeug.utils import secure_filename
import os

admin_success = Blueprint("admin_success", __name__)

@admin_success.route("/admin/casos-de-exito", methods=["GET","POST"])
@login_required
def admin_success_index():
    if current_user.role != "admin":
        return "Acceso denegado", 403

    if request.method == "POST":
        nombre_proyecto = request.form.get("nombre_proyecto", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        industria = request.form.get("industria", "").strip() or None
        # Archivos
        imagen_file = request.files.get("imagen")
        video_file = request.files.get("video")
        logo_file = request.files.get("industria_logo")
        fecha_str = request.form.get("fecha_publicacion", "").strip()
        try:
            fecha_publicacion = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else None
        except ValueError:
            fecha_publicacion = None

        # Guardar archivos si existen
        uploads_root = os.path.join(current_app.static_folder, "uploads")
        os.makedirs(uploads_root, exist_ok=True)
        images_dir = os.path.join(uploads_root, "images")
        videos_dir = os.path.join(uploads_root, "videos")
        logos_dir = os.path.join(uploads_root, "logos")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)
        os.makedirs(logos_dir, exist_ok=True)

        url_imagen = None
        video_url = None
        industria_logo = None

        if imagen_file and imagen_file.filename:
            fname = secure_filename(imagen_file.filename)
            image_path = os.path.join(images_dir, fname)
            imagen_file.save(image_path)
            url_imagen = f"/static/uploads/images/{fname}"

        if video_file and video_file.filename:
            fname = secure_filename(video_file.filename)
            video_path = os.path.join(videos_dir, fname)
            video_file.save(video_path)
            video_url = f"/static/uploads/videos/{fname}"

        if logo_file and logo_file.filename:
            fname = secure_filename(logo_file.filename)
            logo_path = os.path.join(logos_dir, fname)
            logo_file.save(logo_path)
            industria_logo = f"/static/uploads/logos/{fname}"

        if not (nombre_proyecto and descripcion and url_imagen and fecha_publicacion):
            flash("Todos los campos son obligatorios.", "error")
        else:
            create_case(
                nombre_proyecto,
                descripcion,
                url_imagen,
                fecha_publicacion,
                video_url=video_url,
                industria=industria,
                industria_logo=industria_logo,
            )
            flash("Caso creado.", "success")
            return redirect(url_for("admin_success.admin_success_index"))

    cases = list_cases()
    return render_template("admin/casos_exito_crud.html", cases=cases)

@admin_success.route("/admin/casos-de-exito/<int:case_id>/eliminar", methods=["POST"]) 
@login_required
def admin_success_delete(case_id):
    if current_user.role != "admin":
        return "Acceso denegado", 403
    if delete_case(case_id):
        flash("Caso eliminado.", "success")
    else:
        flash("No se encontró el caso.", "error")
    return redirect(url_for("admin_success.admin_success_index"))


@admin_success.route("/admin/casos-de-exito/<int:case_id>/editar", methods=["GET","POST"])
@login_required
def admin_success_edit(case_id):
    if current_user.role != "admin":
        return "Acceso denegado", 403
    item = get_case(case_id)
    if not item:
        flash("Caso no encontrado", "error")
        return redirect(url_for("admin_success.admin_success_index"))

    if request.method == "POST":
        nombre_proyecto = request.form.get("nombre_proyecto", "").strip()
        descripcion = request.form.get("descripcion", "").strip()
        industria = request.form.get("industria", "").strip() or None
        fecha_str = request.form.get("fecha_publicacion", "").strip()
        try:
            fecha_publicacion = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else None
        except ValueError:
            fecha_publicacion = None

        imagen_file = request.files.get("imagen")
        video_file = request.files.get("video")
        logo_file = request.files.get("industria_logo")

        uploads_root = os.path.join(current_app.static_folder, "uploads")
        images_dir = os.path.join(uploads_root, "images")
        videos_dir = os.path.join(uploads_root, "videos")
        logos_dir = os.path.join(uploads_root, "logos")
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)
        os.makedirs(logos_dir, exist_ok=True)

        url_imagen = item.url_imagen
        video_url = item.video_url
        industria_logo = item.industria_logo

        if imagen_file and imagen_file.filename:
            fname = secure_filename(imagen_file.filename)
            imagen_file.save(os.path.join(images_dir, fname))
            url_imagen = f"/static/uploads/images/{fname}"

        if video_file and video_file.filename:
            fname = secure_filename(video_file.filename)
            video_file.save(os.path.join(videos_dir, fname))
            video_url = f"/static/uploads/videos/{fname}"

        if logo_file and logo_file.filename:
            fname = secure_filename(logo_file.filename)
            logo_file.save(os.path.join(logos_dir, fname))
            industria_logo = f"/static/uploads/logos/{fname}"

        if not (nombre_proyecto and descripcion and url_imagen and fecha_publicacion):
            flash("Todos los campos obligatorios.", "error")
        else:
            update_case(
                case_id,
                nombre_proyecto=nombre_proyecto,
                descripcion=descripcion,
                url_imagen=url_imagen,
                fecha_publicacion=fecha_publicacion,
                video_url=video_url,
                industria=industria,
                industria_logo=industria_logo,
            )
            flash("Caso actualizado.", "success")
            return redirect(url_for("admin_success.admin_success_index"))

    return render_template("admin/casos_exito_edit.html", item=item)
