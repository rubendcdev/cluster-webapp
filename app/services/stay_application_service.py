from app.extensions import db
from app.models.stay_application import StayApplication
from typing import List


def create_application(**kwargs) -> StayApplication:
    app = StayApplication(**kwargs)
    db.session.add(app)
    db.session.commit()
    return app


def list_applications() -> List[StayApplication]:
    return StayApplication.query.order_by(StayApplication.created_at.desc()).all()
