from run import app
from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash

def create_super_admin():
    with app.app_context():
        # Datos del Super Admin
        correo = "superadmin@cluster.com"
        pass_plain = "superadmin123"
        
        existing = User.query.filter_by(correo=correo).first()
        if existing:
            print(f"El usuario {correo} ya existe.")
            # Asegurar que tenga el rol correcto
            existing.role = "super_admin"
            db.session.commit()
            print("Rol actualizado a super_admin.")
            return

        new_user = User(
            nombre="Super",
            apellido_paterno="Admin",
            correo=correo,
            password=generate_password_hash(pass_plain),
            role="super_admin"
        )
        db.session.add(new_user)
        db.session.commit()
        print(f"Super Admin creado exitosamente.")
        print(f"Correo: {correo}")
        print(f"Contraseña: {pass_plain}")

if __name__ == "__main__":
    create_super_admin()
