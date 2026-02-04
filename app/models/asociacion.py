from sqlalchemy import Column, Integer, String
from app.extensions import db

class Asociacion(db.Model):
    __tablename__ = "asociaciones"

    idAsociaciones = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(45), nullable=False)
    url_imagen = Column(String(255))
    descripcion = Column(String(255))
    link = Column(String(255))
    tipo = Column(String(20), default='Empresarial') # 'Empresarial' or 'Academica'
