from app.extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    place = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(30), nullable=True)
