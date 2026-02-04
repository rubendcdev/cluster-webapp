# app/controllers/success_cases_controller.py
from flask import Blueprint, render_template
from app.services.success_case_service import list_cases
from app.services.site_config_service import get_config

success_cases = Blueprint("success_cases", __name__)

@success_cases.route("/casos-de-exito")
def casos_de_exito_index():
    cases = list_cases()
    featured = cases[0] if cases else None
    others = cases[1:] if len(cases) > 1 else []
    
    # Obtener el texto informativo sobre estancias
    texto_estancias = get_config("texto_estancias", "")
    
    return render_template("casos de exito/index.html", 
                         featured=featured, 
                         cases=others,
                         texto_estancias=texto_estancias)

