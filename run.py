from flask import Flask
from app.config import Config
from app.extensions import db, login_manager
from app.controllers import (
    public_controller,
    auth_controller,
    admin_gallery_controller
)
from app.models.user import User

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(public_controller.public)
app.register_blueprint(auth_controller.auth)
app.register_blueprint(admin_gallery_controller.admin_gallery)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
