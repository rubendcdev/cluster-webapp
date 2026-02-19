from app.models.gallery import Gallery
from app.extensions import db


def get_all_images():
    return Gallery.query.all()


def get_paginated_images(page: int, per_page: int = 9):
    """Devuelve un objeto de paginación con las imágenes de la galería.

    Usa el método paginate de SQLAlchemy/Flask-SQLAlchemy y ordena por id descendente
    para mostrar primero las imágenes más recientes.
    """
    return Gallery.query.order_by(Gallery.id.desc()).paginate(page=page, per_page=per_page, error_out=False)


def get_image(image_id):
    return Gallery.query.get_or_404(image_id)


def create_image(title, description, image):
    img = Gallery(title=title, description=description, image=image)
    db.session.add(img)
    db.session.commit()
    return img


def update_image(image_id, title=None, description=None, image_filename=None):
    img = Gallery.query.get_or_404(image_id)
    if title is not None:
        img.title = title
    if description is not None:
        img.description = description
    if image_filename is not None:
        img.image = image_filename
    db.session.commit()
    return img


def delete_image(image_id):
    img = Gallery.query.get_or_404(image_id)
    db.session.delete(img)
    db.session.commit()
