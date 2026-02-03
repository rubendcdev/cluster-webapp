from datetime import datetime
from app.extensions import db

class StayApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    apellido_paterno = db.Column(db.String(120), nullable=False)
    apellido_materno = db.Column(db.String(120), nullable=True)
    correo = db.Column(db.String(180), nullable=False)
    telefono = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(120), nullable=False)
    institucion = db.Column(db.String(180), nullable=False)
    cv_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
