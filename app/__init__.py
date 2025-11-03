import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
from flask_login import LoginManager, login_user, UserMixin
from app.infra.database import SessionLocal



# Inicializa as extensões
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """Application factory function."""


    load_dotenv(dotenv_path=".env.local")
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  


 
    CORS(app)

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        # 1. Abre a sessão do DB usando seu padrão SessionLocal
        db_session = SessionLocal() 
        try:
            
            from .models import Usuario 
            user = db_session.get(Usuario, int(user_id))
            return user
            
        except Exception:
             # Em caso de qualquer erro (ex: DB indisponível), o Flask-Login 
            # não deve travar a aplicação. Retornar None é o padrão para falha.
            return None 
        finally:
            # 4. Fechamento Obrigatório da sessão
            db_session.close()

    with app.app_context():
        # ✅ Importações agora são relativas ao pacote 'app'
        from . import models # Importa os modelos para o Alembic encontrá-los
        
        # ✅ Registra os blueprints
        from app.api.health.health_routes import health_bp
        from app.api.home.home_routes import home_bp
        from app.api.projects.projects_routes import project_bp
        from app.api.usuarios.usuario_routes import usuario_bp
        from app.api.auth import auth_bp

        from app.views.adm import admin_bp
        from app.views.home import fhome_bp
        # ... importe os outros blueprints da mesma forma
        
        app.register_blueprint(health_bp, url_prefix="/api")
        app.register_blueprint(home_bp, url_prefix="/api")
        app.register_blueprint(project_bp, url_prefix="/api")
        app.register_blueprint(usuario_bp, url_prefix="/api")
        app.register_blueprint(auth_bp, url_prefix="/api")

        app.register_blueprint(fhome_bp, url_prefix="/")
        app.register_blueprint(admin_bp, url_prefix="/admin")
        
        
        # ... registre os outros

    return app