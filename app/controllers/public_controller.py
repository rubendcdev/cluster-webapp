# app/controllers/public_controller.py
from flask import Blueprint, render_template
from app.services.gallery_service import get_all_images

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
