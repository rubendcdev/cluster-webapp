from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    apellido_paterno = db.Column(db.String(120), nullable=False)
    apellido_materno = db.Column(db.String(120), nullable=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(30), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")
