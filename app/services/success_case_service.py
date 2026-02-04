from app.extensions import db
from app.models.success_case import SuccessCase
from datetime import date


def list_cases():
    return SuccessCase.query.order_by(SuccessCase.fecha_publicacion.desc()).all()


def create_case(
    nombre_proyecto: str,
    descripcion: str,
    url_imagen: str,
    fecha_publicacion: date,
    video_url: str | None = None,
    industria: str | None = None,
    industria_logo: str | None = None,
):
    item = SuccessCase(
        nombre_proyecto=nombre_proyecto,
        descripcion=descripcion,
        url_imagen=url_imagen,
        fecha_publicacion=fecha_publicacion,
        video_url=video_url,
        industria=industria,
        industria_logo=industria_logo,
    )
    db.session.add(item)
    db.session.commit()
    return item


def delete_case(case_id: int):
    item = SuccessCase.query.get(case_id)
    if not item:
        return False
    db.session.delete(item)
    db.session.commit()
    return True


def get_case(case_id: int):
    return SuccessCase.query.get(case_id)


def update_case(case_id: int, **kwargs):
    item = SuccessCase.query.get(case_id)
    if not item:
        return None
    for k, v in kwargs.items():
        if hasattr(item, k) and v is not None:
            setattr(item, k, v)
    db.session.commit()
    return item
