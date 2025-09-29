from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from pathlib import Path
from waitress import serve
from flask_cors import CORS


# Carregar variáveis de ambiente
env_path = Path(__file__).resolve().parent / ".env.local"
load_dotenv(env_path)

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    CORS(app)

    print("DATABASE_URL:", os.getenv("DATABASE_URL"))
    print("SECRET_KEY:", os.getenv("SECRET_KEY"))
    print("Environment Variables:", env_path)

    # Configurações
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Importar modelos para migrations funcionarem
    with app.app_context():
        from models import Project
        from models import Usuario
        print(f"Modelo Project importado: {Project}")
        print(f"Modelo User importado: {Usuario}")

    # ✅ Importar e registrar blueprints
    from api.routes import health_bp, home_bp, project_bp, migrations_bp, usuario_bp, auth_bp

    app.register_blueprint(migrations_bp, url_prefix="/api")
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(home_bp, url_prefix="/") 
    app.register_blueprint(project_bp, url_prefix="/api")
    app.register_blueprint(usuario_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")  # ← registra o blueprint de auth


    

    return app

if __name__ == "__main__":
 app = create_app()   # ← cria a instância da aplicação
 port = int(os.environ.get("PORT", 7000))

 serve(app, host="0.0.0.0", port=port)
