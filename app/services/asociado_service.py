from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.stay_application import StayApplication
from app.models.stay_interest import StayInterest


class AsociadoService:
    @staticmethod
    def get_solicitudes_por_filtro(filtro, user_id):
        """Obtener solicitudes según el filtro (mías o todas)"""
        if filtro == "mias":
            return StayApplication.query.join(StayInterest).filter(
                StayInterest.user_id == user_id
            ).order_by(StayApplication.created_at.desc()).all()
        else:
            return StayApplication.query.order_by(
                StayApplication.created_at.desc()
            ).all()

    @staticmethod
    def marcar_interes(solicitud_id, user_id):
        """Asignar interés de un asociado a una solicitud"""
        solicitud = StayApplication.query.get_or_404(solicitud_id)

        # Verificar si ya está asignada
        if solicitud.stay_interest:
            return False, "Esta solicitud ya fue tomada por otro asociado.", "warning"

        interes = StayInterest(
            user_id=user_id,
            stay_application_id=solicitud.id
        )

        db.session.add(interes)

        try:
            db.session.commit()
            return True, "Solicitud asignada correctamente.", "success"
        except IntegrityError:
            db.session.rollback()
            return False, "Otro asociado la tomó antes que tú.", "warning"

    @staticmethod
    def liberar_interes(solicitud_id, user_id):
        """Liberar el interés de un asociado en una solicitud"""
        interes = StayInterest.query.filter_by(
            stay_application_id=solicitud_id,
            user_id=user_id
        ).first()

        if not interes:
            return False, "No puedes liberar esta solicitud.", "warning"

        db.session.delete(interes)
        db.session.commit()

        return True, "Solicitud liberada correctamente.", "success"
