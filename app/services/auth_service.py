from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash

def register_user(nombre, apellido_paterno, apellido_materno, correo, telefono, password):
    user = User(
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno or None,
        correo=correo,
        telefono=telefono or None,
        password=generate_password_hash(password),
        role="user"
    )
    db.session.add(user)
    db.session.commit()
