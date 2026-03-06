import os
import time
from werkzeug.utils import secure_filename
from flask import current_app
from app.models.curso import Curso
from app.extensions import db


class CursoService:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in CursoService.ALLOWED_EXTENSIONS

    @staticmethod
    def save_image(file):
        """Guarda la imagen subida en la carpeta uploads/cursos y retorna el nombre del archivo"""
        if file and file.filename != '' and CursoService.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = str(int(time.time()))
            imagen_filename = f"{timestamp}_{filename}"

            upload_dir = os.path.join(current_app.static_folder, 'uploads', 'cursos')
            os.makedirs(upload_dir, exist_ok=True)

            file.save(os.path.join(upload_dir, imagen_filename))
            return imagen_filename
        return None

    @staticmethod
    def delete_old_image(url_imagen):
        """Elimina una imagen antigua si existe en el disco"""
        if url_imagen and not url_imagen.startswith('http'):
            image_path = os.path.join(current_app.static_folder, 'uploads', 'cursos', url_imagen)
            if os.path.exists(image_path):
                os.remove(image_path)

    @staticmethod
    def get_all_cursos():
        return Curso.query.all()

    @staticmethod
    def get_curso_by_id(curso_id):
        return Curso.query.get_or_404(curso_id)

    @staticmethod
    def create_curso(nombre, descripcion, link, image_file):
        """Crea un nuevo curso, manejando también la subida de imagen."""
        if not nombre:
            return False, "El nombre es obligatorio", "danger"

        imagen_filename = CursoService.save_image(image_file)

        nuevo_curso = Curso(
            nombre=nombre,
            url_imagen=imagen_filename,
            descripcion=descripcion,
            link=link
        )

        db.session.add(nuevo_curso)
        db.session.commit()

        return True, "Curso creado exitosamente", "success"

    @staticmethod
    def update_curso(curso_id, nombre, descripcion, link, image_file):
        """Actualiza un curso existente y maneja la imagen."""
        if not nombre:
            return False, "El nombre es obligatorio", "danger"

        curso = Curso.query.get_or_404(curso_id)

        if image_file and image_file.filename != '':
            # Eliminar imagen vieja
            CursoService.delete_old_image(curso.url_imagen)
            # Guardar imagen nueva
            imagen_filename = CursoService.save_image(image_file)
            if imagen_filename:
                curso.url_imagen = imagen_filename

        curso.nombre = nombre
        curso.descripcion = descripcion
        curso.link = link

        db.session.commit()

        return True, "Curso actualizado exitosamente", "success"

    @staticmethod
    def delete_curso(curso_id):
        """Elimina un curso y su imagen asociada."""
        curso = Curso.query.get_or_404(curso_id)

        CursoService.delete_old_image(curso.url_imagen)

        db.session.delete(curso)
        db.session.commit()

        return True, "Curso eliminado exitosamente", "success"
