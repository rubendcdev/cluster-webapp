from app.extensions import db
from datetime import datetime

class SiteConfig(db.Model):
    """Modelo para almacenar configuraciones del sitio"""
    __tablename__ = 'site_config'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SiteConfig {self.key}>'
