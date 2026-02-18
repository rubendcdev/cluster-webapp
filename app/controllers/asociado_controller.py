from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.stay_application import StayApplication
from app.models.stay_interest import StayInterest

asociado = Blueprint("asociado", __name__, url_prefix="/asociado")


@asociado.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "asociado":
        abort(403)

    filtro = request.args.get("filtro")

    if filtro == "mias":
        solicitudes = StayApplication.query.join(StayInterest).filter(
            StayInterest.user_id == current_user.id
        ).order_by(StayApplication.created_at.desc()).all()
    else:
        solicitudes = StayApplication.query.order_by(
            StayApplication.created_at.desc()
        ).all()

    return render_template(
        "asociado/dashboard.html",
        solicitudes=solicitudes
    )


@asociado.route("/solicitudes/<int:id>/interes", methods=["POST"])
@login_required
def marcar_interes(id):
    if current_user.role != "asociado":
        abort(403)

    solicitud = StayApplication.query.get_or_404(id)

    # Verificar si ya está asignada
    if solicitud.stay_interest:
        flash("Esta solicitud ya fue tomada por otro asociado.", "warning")
        return redirect(url_for("asociado.dashboard"))

    interes = StayInterest(
        user_id=current_user.id,
        stay_application_id=solicitud.id
    )

    db.session.add(interes)

    try:
        db.session.commit()
        flash("Solicitud asignada correctamente.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("Otro asociado la tomó antes que tú.", "warning")

    return redirect(url_for("asociado.dashboard"))

@asociado.route("/solicitudes/<int:id>/liberar", methods=["POST"])
@login_required
def liberar_interes(id):
    if current_user.role != "asociado":
        abort(403)

    interes = StayInterest.query.filter_by(
        stay_application_id=id,
        user_id=current_user.id
    ).first()

    if not interes:
        flash("No puedes liberar esta solicitud.", "warning")
        return redirect(url_for("asociado.dashboard"))

    db.session.delete(interes)
    db.session.commit()

    flash("Solicitud liberada correctamente.", "success")
    return redirect(url_for("asociado.dashboard"))