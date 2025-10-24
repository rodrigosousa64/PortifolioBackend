# routes/usuario_routes.py
from flask import Blueprint
from app.controllers.usuario_controller import UsuarioController

usuario_bp = Blueprint("usuarios", __name__)

# CRUD routes
@usuario_bp.route("/usuarios", methods=["GET"])
def get_all_users():
    return UsuarioController.get_all_users()

@usuario_bp.route("/usuarios/<int:user_id>", methods=["GET"])
def get_user(user_id):
    return UsuarioController.get_user(user_id)

@usuario_bp.route("/usuarios", methods=["POST"])
def create_user():
    return UsuarioController.create_user()

@usuario_bp.route("/usuarios/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    return UsuarioController.update_user(user_id)

@usuario_bp.route("/usuarios/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    return UsuarioController.delete_user(user_id)
