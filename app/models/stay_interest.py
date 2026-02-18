from datetime import datetime
from app.extensions import db


class StayInterest(db.Model):
    __tablename__ = "stay_interest"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    stay_application_id = db.Column(
        db.Integer,
        db.ForeignKey("stay_application.id"),
        nullable=False,
        unique=True  # 🔒 solo un asociado por solicitud
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    user = db.relationship("User", backref="stay_interests")
    stay_application = db.relationship(
        "StayApplication",
        backref=db.backref("stay_interest", uselist=False)
    )
