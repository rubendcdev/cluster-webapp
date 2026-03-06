from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user

from app.services.asociado_service import AsociadoService

asociado = Blueprint("asociado", __name__, url_prefix="/asociado")


@asociado.route("/dashboard")
@login_required
def dashboard():
    if current_user.role != "asociado":
        abort(403)

    filtro = request.args.get("filtro")
    solicitudes = AsociadoService.get_solicitudes_por_filtro(filtro, current_user.id)

    return render_template(
        "asociado/dashboard.html",
        solicitudes=solicitudes
    )


@asociado.route("/solicitudes/<int:id>/interes", methods=["POST"])
@login_required
def marcar_interes(id):
    if current_user.role != "asociado":
        abort(403)

    success, message, category = AsociadoService.marcar_interes(id, current_user.id)
    flash(message, category)

    return redirect(url_for("asociado.dashboard"))


@asociado.route("/solicitudes/<int:id>/liberar", methods=["POST"])
@login_required
def liberar_interes(id):
    if current_user.role != "asociado":
        abort(403)

    success, message, category = AsociadoService.liberar_interes(id, current_user.id)
    flash(message, category)

    return redirect(url_for("asociado.dashboard"))
