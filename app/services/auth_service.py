from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash

def register_user(username, email, password):
    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        role="user"
    )
    db.session.add(user)
    db.session.commit()
