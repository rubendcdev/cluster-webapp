from flask_login import login_required, current_user
from flask import Blueprint, request, redirect, url_for, abort
from app.services.event_service import save, update, delete   # ejemplo import

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
        date_str=request.form["date"]
    )

    return redirect(url_for("public.events"))

@events.route("/event/<int:event_id>/update", methods=["POST"])
@login_required
def update_event(event_id):

    if current_user.role != "admin":
        abort(403)

    update(
        event_id=event_id,
        title=request.form["title"],
        description=request.form.get("description"),
        place=request.form["place"],
        date_str=request.form["date"]
    )

    return redirect(url_for("public.events"))

@events.route("/event/<int:event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):

    if current_user.role != "admin":
        abort(403)

    delete(event_id)

    return redirect(url_for("public.events"))