from app.extensions import db

class SuccessCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_proyecto = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    url_imagen = db.Column(db.String(255), nullable=False)
    fecha_publicacion = db.Column(db.Date, nullable=False)
    # Opcionales para enriquecer la vista
    video_url = db.Column(db.String(255))
    industria = db.Column(db.String(120))
    industria_logo = db.Column(db.String(255))
