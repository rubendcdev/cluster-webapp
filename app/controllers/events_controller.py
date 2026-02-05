from flask_login import login_required, current_user
from flask import Blueprint, request, redirect, url_for, abort
from app.services.event_service import save   # ejemplo import

events = Blueprint("events", __name__)

@events.route("/event/create", methods=["POST"])
@login_required
def create_event():

    if current_user.role != "admin":
        abort(403)

    save(
        title=request.form["title"],
        description=request.form.get("description"),
        place=request.form["place"],
        date=request.form.get("date")
    )

    return redirect(url_for("public.events"))
