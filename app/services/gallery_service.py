from app.models.gallery import Gallery
from app.extensions import db

def get_all_images():
    return Gallery.query.all()

def create_image(title, description, image):
    img = Gallery(title=title, description=description, image=image)
    db.session.add(img)
    db.session.commit()
