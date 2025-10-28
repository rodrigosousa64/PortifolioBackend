from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # <--- NOVIDADE: Necessário para Flask-Login


# A classe Usuario DEVE herdar de db.Model E UserMixin
class Usuario(db.Model, UserMixin): 
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False) # Permissão de Admin

    # ----------------------------------------------------------------------
    # O UserMixin fornece automaticamente: is_active, is_authenticated, is_anonymous, get_id()
    # ----------------------------------------------------------------------
    
    def __repr__(self):
        return f"<Usuario id={self.id} name='{self.name}' is_admin={self.is_admin}>"

    # setters e getters para senha
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_admin": self.is_admin
        }
