# Importações necessárias:
from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user # A chave!

def admin_required(f):
    # Seu código do decorador aqui (o código que verifica current_user.is_admin)
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            # Caso não esteja logado, redireciona para o login
            # (Ajuste o nome do endpoint 'auth_bp.login' conforme seu Blueprint de login)
            flash('Acesso restrito. Por favor, faça login.', 'warning')
            return redirect(url_for('usuario_bp.login_user')) 
        
        if not current_user.is_admin:
            # Não é admin, retorna 403 Forbidden
            return abort(403) 
            
        return f(*args, **kwargs)
    return decorated_function