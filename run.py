from flask import Flask
from app.config import Config
from app.extensions import db, login_manager
from app.controllers import (
    events_controller,
    public_controller,
    auth_controller,
    admin_gallery_controller,
    asociaciones_controller,
    cursos_controller,
    success_cases_controller,
    admin_success_cases_controller,
    stay_application_controller,
    admin_site_config_controller,
    super_admin_controller
)
from app.models.user import User
from app.models.asociacion import Asociacion
from app.models.curso import Curso

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
app.register_blueprint(events_controller.events)
app.register_blueprint(auth_controller.auth)
app.register_blueprint(admin_gallery_controller.admin_gallery)
app.register_blueprint(asociaciones_controller.asociaciones)
app.register_blueprint(cursos_controller.cursos)
app.register_blueprint(success_cases_controller.success_cases)
app.register_blueprint(admin_success_cases_controller.admin_success)
app.register_blueprint(stay_application_controller.stay_app)
app.register_blueprint(admin_site_config_controller.admin_site_config)
app.register_blueprint(super_admin_controller.super_admin)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
