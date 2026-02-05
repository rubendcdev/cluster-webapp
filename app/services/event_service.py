from app.extensions import db
from app.models.event import Event

def get_all():
    return Event.query.all()

def save(
        title: str,
        description: str,
        place: str,
        date: str
):
    event = Event(
        title = title,
        description = description,
        place = place,
        date = date
    )

    db.session.add(event)
    db.session.commit()
    return event