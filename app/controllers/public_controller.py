# app/controllers/public_controller.py
from datetime import date
from flask import Blueprint, render_template, request
from app.services.gallery_service import get_paginated_images
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
    page = request.args.get("page", 1, type=int)
    pagination = get_paginated_images(page=page, per_page=9)
    images = pagination.items
    return render_template("gallery/index.html", images=images, pagination=pagination)

@public.route("/events")
def events():
    today = date.today().isoformat()
    events = get_all()
    return render_template("events.html", events = events, today = today)