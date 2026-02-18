from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash

def register_user(nombre, apellido_paterno, apellido_materno, correo, telefono, password, nombre_empresa=None, role="user"):
    user = User(
        nombre=nombre or None,
        apellido_paterno=apellido_paterno or None,
        apellido_materno=apellido_materno or None,
        nombre_empresa=nombre_empresa or None,
        correo=correo,
        telefono=telefono or None,
        password=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()
