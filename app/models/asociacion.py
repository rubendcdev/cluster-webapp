from sqlalchemy import Column, Integer, String
from database import Base 

class Asociacion(Base):
    __tablename__ = "asociaciones"

    idAsociaciones = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(45), nullable=False)
    url_imagen = Column(String(255))
    descripcion = Column(String(255))
    link = Column(String(255))
