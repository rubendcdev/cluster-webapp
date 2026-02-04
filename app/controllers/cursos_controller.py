from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models.curso import Curso
from app.extensions import db

cursos = Blueprint("cursos", __name__, url_prefix="/cursos")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_image_url(curso):
    """Helper function to get the correct image URL"""
    if not curso.url_imagen:
        return None
    
    # If it's an external URL (starts with http)
    if curso.url_imagen.startswith('http'):
        return curso.url_imagen
    
    # If it's a local file, use url_for with static path
    return url_for('static', filename=f'uploads/cursos/{curso.url_imagen}')

@cursos.route("/")
def index():
    """List all cursos"""
    cursos_list = Curso.query.all()
    return render_template("cursos/index.html", cursos=cursos_list)

@cursos.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new curso"""
    if current_user.role != "admin":
        flash("Solo los administradores pueden crear cursos", "danger")
        return redirect(url_for("cursos.index"))
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        link = request.form.get("link")
        
        # Handle file upload
        imagen_filename = None
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                import time
                timestamp = str(int(time.time()))
                imagen_filename = f"{timestamp}_{filename}"
                
                # Create upload directory if it doesn't exist
                upload_dir = os.path.join(current_app.static_folder, 'uploads', 'cursos')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Save the file
                file.save(os.path.join(upload_dir, imagen_filename))
        
        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return render_template("cursos/create.html")
        
        nuevo_curso = Curso(
            nombre=nombre,
            url_imagen=imagen_filename,
            descripcion=descripcion,
            link=link
        )
        
        db.session.add(nuevo_curso)
        db.session.commit()
        
        flash("Curso creado exitosamente", "success")
        return redirect(url_for("cursos.index"))
    
    return render_template("cursos/create.html")

@cursos.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    """Edit an existing curso"""
    if current_user.role != "admin":
        flash("Solo los administradores pueden editar cursos", "danger")
        return redirect(url_for("cursos.index"))
    
    curso = Curso.query.get_or_404(id)
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        link = request.form.get("link")
        
        # Handle file upload
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file and file.filename != '' and allowed_file(file.filename):
                # Delete old image if exists
                if curso.url_imagen and not curso.url_imagen.startswith('http'):
                    old_image_path = os.path.join(current_app.static_folder, 'uploads', 'cursos', curso.url_imagen)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                import time
                timestamp = str(int(time.time()))
                imagen_filename = f"{timestamp}_{filename}"
                
                # Create upload directory if it doesn't exist
                upload_dir = os.path.join(current_app.static_folder, 'uploads', 'cursos')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Save the file
                file.save(os.path.join(upload_dir, imagen_filename))
                curso.url_imagen = imagen_filename
        
        if not nombre:
            flash("El nombre es obligatorio", "danger")
            return render_template("cursos/edit.html", curso=curso)
        
        curso.nombre = nombre
        curso.descripcion = descripcion
        curso.link = link
        
        db.session.commit()
        
        flash("Curso actualizado exitosamente", "success")
        return redirect(url_for("cursos.index"))
    
    return render_template("cursos/edit.html", curso=curso)

@cursos.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    """Delete a curso"""
    if current_user.role != "admin":
        flash("Solo los administradores pueden eliminar cursos", "danger")
        return redirect(url_for("cursos.index"))
    
    curso = Curso.query.get_or_404(id)
    
    # Delete image file if exists
    if curso.url_imagen and not curso.url_imagen.startswith('http'):
        image_path = os.path.join(current_app.static_folder, 'uploads', 'cursos', curso.url_imagen)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(curso)
    db.session.commit()
    
    flash("Curso eliminado exitosamente", "success")
    return redirect(url_for("cursos.index"))

@cursos.route("/<int:id>")
def show(id):
    """Show details of a specific curso"""
    curso = Curso.query.get_or_404(id)
    return render_template("cursos/show.html", curso=curso)
