from .health_routes import health_bp
from .home_routes import home_bp
from .projects_routes import project_bp
from .migrations_routes import migrations_bp
from .usuario_routes import usuario_bp
from app.api.auth import auth_bp

__all__ = ['health_bp', 'home_bp', 'project_bp', 'migrations_bp', 'usuario_bp', 'auth_bp']