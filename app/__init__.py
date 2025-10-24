import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

# Inicializa as extensões sem uma aplicação ainda
db = SQLAlchemy()
migrate = Migrate()

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

    with app.app_context():
        # ✅ Importações agora são relativas ao pacote 'app'
        from . import models # Importa os modelos para o Alembic encontrá-los
        
        # ✅ Registra os blueprints
        from app.api.routes.health_routes import health_bp
        from app.api.routes.home_routes import home_bp
        from app.api.routes.projects_routes import project_bp
        from app.api.routes.usuario_routes import usuario_bp
        # ... importe os outros blueprints da mesma forma
        
        app.register_blueprint(health_bp, url_prefix="/api")
        app.register_blueprint(home_bp, url_prefix="/")
        app.register_blueprint(project_bp, url_prefix="/api")
        app.register_blueprint(usuario_bp, url_prefix="/api")
        # ... registre os outros

    return app