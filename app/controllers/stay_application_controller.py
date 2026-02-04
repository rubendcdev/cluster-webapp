# app/controllers/stay_application_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename
import os
from app.services.stay_application_service import create_application

stay_app = Blueprint("stay_app", __name__)

@stay_app.route("/solicitud-estadia", methods=["GET", "POST"])
@login_required
def stay_application_form():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        apellido_paterno = request.form.get("apellido_paterno", "").strip()
        apellido_materno = request.form.get("apellido_materno", "").strip()
        correo = request.form.get("correo", "").strip().lower()
        telefono = request.form.get("telefono", "").strip()
        estado = request.form.get("estado", "").strip()
        institucion = request.form.get("institucion", "").strip()
        cv_file = request.files.get("cv")

        # Validaciones básicas
        if not (nombre and apellido_paterno and correo and telefono and estado and institucion and cv_file and cv_file.filename):
            flash("Todos los campos marcados y el CV son obligatorios.", "error")
            return render_template("solicitudes/estadia_form.html"), 400

        uploads_root = os.path.join(current_app.static_folder, "uploads")
        cv_dir = os.path.join(uploads_root, "cv")
        os.makedirs(cv_dir, exist_ok=True)
        cv_name = secure_filename(cv_file.filename)
        cv_path = os.path.join(cv_dir, cv_name)
        cv_file.save(cv_path)

        app_obj = create_application(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            correo=correo,
            telefono=telefono,
            estado=estado,
            institucion=institucion,
            cv_path=f"/static/uploads/cv/{cv_name}",
        )
        flash("Tu solicitud fue registrada. ¡Gracias!", "success")
        return redirect(url_for("stay_app.stay_application_form"))

    return render_template("solicitudes/estadia_form.html")
