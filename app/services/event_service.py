from datetime import datetime
from app.extensions import db
from app.models.event import Event

def get_all():
    return Event.query.all()

def get_by_id(event_id: int):
    return Event.query.get_or_404(event_id)

def save(
    title: str,
    description: str,
    place: str,
    date_str: str
):
    event_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    event = Event(
        title=title,
        description=description,
        place=place,
        date=event_date
    )

    db.session.add(event)
    db.session.commit()

    return event

def update(
    event_id: int,
    title: str,
    description: str,
    place: str,
    date_str: str
):
    event = get_by_id(event_id)

    event_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    event.title = title
    event.description = description
    event.place = place
    event.date = event_date

    db.session.commit()

    return event

def delete(event_id: int):
    event = get_by_id(event_id)

    db.session.delete(event)
    db.session.commit()

    return True