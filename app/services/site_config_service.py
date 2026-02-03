# app/services/site_config_service.py
from app.models.site_config import SiteConfig
from app.extensions import db

def get_config(key, default=None):
    """Obtiene una configuración por su clave"""
    config = SiteConfig.query.filter_by(key=key).first()
    return config.value if config else default

def set_config(key, value):
    """Actualiza o crea una configuración"""
    config = SiteConfig.query.filter_by(key=key).first()
    if config:
        config.value = value
    else:
        config = SiteConfig(key=key, value=value)
        db.session.add(config)
    db.session.commit()
    return config

def get_all_configs():
    """Obtiene todas las configuraciones"""
    return SiteConfig.query.all()
