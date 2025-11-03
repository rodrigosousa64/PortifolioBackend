from ..health.health_routes import health_bp
from ..home.home_routes import home_bp
from ..projects.projects_routes import project_bp
from ..migrates.migrations_routes import migrations_bp
from ..usuarios.usuario_routes import usuario_bp
from app.api.auth import auth_bp

__all__ = ['health_bp', 'home_bp', 'project_bp', 'migrations_bp', 'usuario_bp', 'auth_bp']