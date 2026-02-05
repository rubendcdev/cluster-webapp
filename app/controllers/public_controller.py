# app/controllers/public_controller.py
from flask import Blueprint, render_template
from app.services.gallery_service import get_all_images
from app.services.event_service import get_all

public = Blueprint("public", __name__)

@public.route("/")
def index():
    return render_template("index.html")

@public.route("/about")
def about():
    return render_template("about.html")

@public.route("/gallery")
def gallery():
    images = get_all_images()
    return render_template("gallery.html", images=images)

@public.route("/events")
def events():
    events = get_all()
    return render_template("events.html", events = events)