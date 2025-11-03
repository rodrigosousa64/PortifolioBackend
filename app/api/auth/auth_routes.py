from flask import Blueprint, jsonify, request
from flask_login import login_user, current_user, logout_user, login_required
from app.infra.database import SessionLocal # Seu padrão de DB
from app.models.usuario_models import Usuario
from app.api.auth import auth_bp # Assume que o modelo é importável
# Você também precisará importar o db se estiver usando db.session em outras partes:
# from app.extensoes import db 



# --- ROTA SIMPLES DE TESTE ---
@auth_bp.route('/hello', methods=['GET'])
def auth_index():
    """Verifica se o Blueprint está funcionando."""
    return jsonify({"message": "Auth Blueprint is working!"}), 200

# --- ROTA DE LOGIN (POST) ---
@auth_bp.route('/login', methods=['POST'])
def login_route():
    """Lida com a autenticação do usuário e estabelece o cookie de sessão."""
    
    # 1. Abre a sessão do DB, seguindo seu padrão SessionLocal
    db_session = SessionLocal() 
    try:
        data = request.get_json()
        
        # 1.1. Validação de dados de entrada
        if not data or not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password are required"}), 400
        
        email = data["email"]
        password = data["password"]

        # 2. Busca e autentica o usuário (usando a sessão aberta)
        # O .filter_by() com first() é a forma correta de buscar
        user = db_session.query(Usuario).filter_by(email=email).first()
        
        # 3. Verifica as credenciais (existência e senha)
        if not user or not user.check_password(password):
            return jsonify({"error": "Invalid credentials"}), 401

        # 4. CONEXÃO CRÍTICA: Estabelece o Cookie de Sessão
        # O Flask-Login armazena o ID do usuário no cookie.
        login_user(user) 
        
        # 5. Retorna a confirmação
        return jsonify({
            "message": "Login successful (Cookie Set)", 
            "user_id": user.id,
            "is_admin": user.is_admin 
        }), 200
        
    except Exception as e:
        # Em caso de erro, você pode querer logar o 'e' para debug
        return jsonify({"error": "Login failed due to server error.", "details": str(e)}), 500
    finally:
        # 6. Fechamento Obrigatório da Sessão do DB
        db_session.close()

# --- ROTA DE LOGOUT ---
@auth_bp.route('/logout', methods=['POST'])
@login_required # Só quem está logado pode fazer logout
def logout_route():
    """Encerra a sessão do usuário."""
    logout_user()
    return jsonify({"message": "Logout successful"}), 200

# --- ROTA DE STATUS DO USUÁRIO (OPCIONAL) ---
@auth_bp.route('/status', methods=['GET'])
def status_route():
    """Verifica se o usuário está autenticado e retorna seus dados."""
    if current_user.is_authenticated:
        # current_user é o objeto Usuario que o user_loader buscou
        return jsonify({
            "is_logged_in": True,
            "user_id": current_user.id,
            "email": current_user.email,
            "is_admin": current_user.is_admin
        }), 200
    else:
        return jsonify({"is_logged_in": False, "message": "User is not authenticated"}), 401
