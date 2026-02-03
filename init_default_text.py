# Script para inicializar el texto informativo por defecto
from app.extensions import db
from app.models.site_config import SiteConfig

def init_default_text():
    """Inicializa el texto informativo por defecto sobre estancias"""
    
    texto_default = """Apoyamos a jóvenes de la Universidad Tecnológica de la Selva en Chiapas y a la Universidad Tecnológica de Manzanillo para venir a Guadalajara para sus estancias profesionales.

Se trata de un proceso de 4 meses en el que trabajan en nuestras empresas en temas relacionados con su carrera como requisito para la graduación para que puedan adquirir experiencia en empresas reales y complementar su educación universitaria. Tenemos un doble beneficio, además de apoyarlos, encontramos jóvenes con mucho talento, muy comprometidos, excelentes colaboradores y sobre todo, el deseo de salir adelante.

Para el próximo ciclo MAYO - AGOSTO, queremos seguir apoyando a los jóvenes por lo que estamos buscando empresas que estén interesadas en participar y convertirse en talento humano.

La mecánica es que nos envíes un correo electrónico con la intención de tener 1 o más chicos en tus empresas y el perfil que requieran, que provienen de Áreas Administrativas, Tecnologías de la Información, Turismo, Gastronomía y Alimentación.

Vía Cluster te ofrecemos un lugar para vivir, así como dinero para comida y transporte mientras estés en Guadalajara. Te hacemos firmar las reglas (*) de convivencia y te las presentamos para que puedas empezar a trabajar.

Los problemas de IMSS se cubren a través de un seguro opcional proporcionado por la Universidad. Periódicamente le pedimos que evalúe a los niños para que reciban retroalimentación y que al final servirá para el grado dado por la Universidad para que puedan graduarse."""
    
    # Verificar si ya existe
    existing = SiteConfig.query.filter_by(key='texto_estancias').first()
    
    if not existing:
        config = SiteConfig(key='texto_estancias', value=texto_default)
        db.session.add(config)
        db.session.commit()
        print("✓ Texto informativo inicializado correctamente")
    else:
        print("✓ El texto informativo ya existe en la base de datos")

if __name__ == "__main__":
    from run import app
    with app.app_context():
        init_default_text()
