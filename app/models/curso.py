
from sqlalchemy import Column, Integer, String
from app.extensions import db

class Curso(db.Model):
    __tablename__ = "Cursos"

    idCursos = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    descripcion = db.Column(db.String(255))
    link = db.Column(db.String(255))
    url_imagen = Column(String(255))

    def __repr__(self):
        return f"<Curso {self.nombre}>"
