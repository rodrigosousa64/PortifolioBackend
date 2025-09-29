# routes/auth_routes.py
from flask import Blueprint
from controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

# Registro
@auth_bp.route("/auth/register", methods=["POST"])
def register_user():
    return AuthController.register_user()

# Login
@auth_bp.route("/auth/login", methods=["POST"])
def login_user():
    return AuthController.login_user()

# Logout
@auth_bp.route("/auth/logout", methods=["POST"])
def logout_user():
    return AuthController.logout_user()
