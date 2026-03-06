from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.services.curso_service import CursoService

cursos = Blueprint("cursos", __name__, url_prefix="/cursos")

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
    cursos_list = CursoService.get_all_cursos()
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
        image_file = request.files.get('imagen')
        
        success, message, category = CursoService.create_curso(nombre, descripcion, link, image_file)
        
        flash(message, category)
        if success:
            return redirect(url_for("cursos.index"))
        else:
            return render_template("cursos/create.html")
    
    return render_template("cursos/create.html")

@cursos.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    """Edit an existing curso"""
    if current_user.role != "admin":
        flash("Solo los administradores pueden editar cursos", "danger")
        return redirect(url_for("cursos.index"))
    
    curso = CursoService.get_curso_by_id(id)
    
    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        link = request.form.get("link")
        image_file = request.files.get('imagen')
        
        success, message, category = CursoService.update_curso(id, nombre, descripcion, link, image_file)
        
        flash(message, category)
        if success:
            return redirect(url_for("cursos.index"))
        else:
            return render_template("cursos/edit.html", curso=curso)
    
    return render_template("cursos/edit.html", curso=curso)

@cursos.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    """Delete a curso"""
    if current_user.role != "admin":
        flash("Solo los administradores pueden eliminar cursos", "danger")
        return redirect(url_for("cursos.index"))
    
    success, message, category = CursoService.delete_curso(id)
    flash(message, category)
    
    return redirect(url_for("cursos.index"))

@cursos.route("/<int:id>")
def show(id):
    """Show details of a specific curso"""
    curso = CursoService.get_curso_by_id(id)
    return render_template("cursos/show.html", curso=curso)

