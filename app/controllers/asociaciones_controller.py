from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models.asociacion import Asociacion
from app.extensions import db

asociaciones = Blueprint("asociaciones", __name__, url_prefix="/asociaciones")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_url(asociacion):
    """Helper function to get the correct image URL"""
    if not asociacion.url_imagen:
        return None
    
    # If it's an external URL (starts with http)
    if asociacion.url_imagen.startswith('http'):
        return asociacion.url_imagen
    
    # If it's a local file, use url_for with static path
    return url_for('static', filename=f'uploads/asociaciones/{asociacion.url_imagen}')

@asociaciones.route("/")
def index():
    """List all asociaciones split by type"""
    all_asociaciones = Asociacion.query.all()
    empresariales = [a for a in all_asociaciones if a.tipo == 'Empresarial' or a.tipo is None]
    academicas = [a for a in all_asociaciones if a.tipo == 'Academica']
    
    return render_template("asociaciones/index.html", 
                         empresariales=empresariales, 
                         academicas=academicas,
                         asociaciones=all_asociaciones) # Keep this for backward compatibility if needed

@asociaciones.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new asociacion"""
    if current_user.role != "admin":
        flash("Solo los administradores pueden crear asociaciones", "danger")
        return redirect(url_for("asociaciones.index"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        link = request.form.get("link")
        tipo = request.form.get("tipo", "Empresarial")
        
        # Handle file upload
        imagen_filename = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            print(f"Archivo recibido: {file}")
            print(f"Nombre del archivo: {file.filename}")
            print(f"Tipo de contenido: {file.content_type}")
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(f"Nombre seguro del archivo: {filename}")
                # Add timestamp to avoid filename conflicts
                import time
                timestamp = str(int(time.time()))
                imagen_filename = f"{timestamp}_{filename}"
                
                # Create upload directory if it doesn't exist
                upload_dir = os.path.join(current_app.static_folder, 'uploads', 'asociaciones')
                os.makedirs(upload_dir, exist_ok=True)
                print(f"Directorio de upload: {upload_dir}")
                
                # Save the file
                file.save(os.path.join(upload_dir, imagen_filename))
                print(f"Imagen guardada en: {os.path.join(upload_dir, imagen_filename)}")
                print(f"El archivo existe: {os.path.exists(os.path.join(upload_dir, imagen_filename))}")
            else:
                print("Validación del archivo falló o el nombre está vacío")
        else:
            print("No se encontró el campo 'imagen' en request.files")
        
        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return render_template("asociaciones/create.html")
        
        nueva_asociacion = Asociacion(
            nombre=nombre,
            url_imagen=imagen_filename,
            descripcion=descripcion,
            link=link,
            tipo=tipo
        )
        
        db.session.add(nueva_asociacion)
        db.session.commit()
        
        flash("Asociación creada exitosamente", "success")
        return redirect(url_for("asociaciones.index"))
    
    return render_template("asociaciones/create.html")

@asociaciones.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    """Edit an existing asociacion"""
    if current_user.role != "admin":
        flash("Solo los administradores pueden editar asociaciones", "danger")
        return redirect(url_for("asociaciones.index"))
    
    asociacion = Asociacion.query.get_or_404(id)
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        link = request.form.get("link")
        tipo = request.form.get("tipo", "Empresarial")
        
        # Handle file upload
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old image if exists
                if asociacion.url_imagen and not asociacion.url_imagen.startswith('http'):
                    old_image_path = os.path.join(current_app.static_folder, 'uploads', 'asociaciones', asociacion.url_imagen)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                import time
                timestamp = str(int(time.time()))
                imagen_filename = f"{timestamp}_{filename}"
                
                # Create upload directory if it doesn't exist
                upload_dir = os.path.join(current_app.static_folder, 'uploads', 'asociaciones')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Save the file
                file.save(os.path.join(upload_dir, imagen_filename))
                print(f"Imagen guardada en: {os.path.join(upload_dir, imagen_filename)}")
                print(f"El archivo existe: {os.path.exists(os.path.join(upload_dir, imagen_filename))}")
                asociacion.url_imagen = imagen_filename
            # Si no se sube archivo, mantener la imagen existente (no hacer nada)
        
        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return render_template("asociaciones/edit.html", asociacion=asociacion)
        
        asociacion.nombre = nombre
        asociacion.descripcion = descripcion
        asociacion.link = link
        asociacion.tipo = tipo
        
        db.session.commit()
        
        flash("Asociación actualizada exitosamente", "success")
        return redirect(url_for("asociaciones.index"))
    
    return render_template("asociaciones/edit.html", asociacion=asociacion)

@asociaciones.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    """Delete an asociacion"""
    if current_user.role != "admin":
        flash("Solo los administradores pueden eliminar asociaciones", "danger")
        return redirect(url_for("asociaciones.index"))
    
    asociacion = Asociacion.query.get_or_404(id)
    
    # Delete image file if exists
    if asociacion.url_imagen and not asociacion.url_imagen.startswith('http'):
        image_path = os.path.join(current_app.static_folder, 'uploads', 'asociaciones', asociacion.url_imagen)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(asociacion)
    db.session.commit()
    
    flash("Asociación eliminada exitosamente", "success")
    return redirect(url_for("asociaciones.index"))

@asociaciones.route("/<int:id>")
def show(id):
    """Show details of a specific asociacion"""
    asociacion = Asociacion.query.get_or_404(id)
    return render_template("asociaciones/show.html", asociacion=asociacion)
