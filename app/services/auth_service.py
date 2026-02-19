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

def update_user(user_id, nombre, apellido_paterno, apellido_materno, correo, telefono, password=None, role=None):
    user = User.query.get_or_404(user_id)

    user.nombre = nombre or None
    user.apellido_paterno = apellido_paterno or None
    user.apellido_materno = apellido_materno or None
    user.correo = correo
    user.telefono = telefono or None

    if password:
        user.password = generate_password_hash(password)

    if role:
        user.role = role

    db.session.commit()
    return user


def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()