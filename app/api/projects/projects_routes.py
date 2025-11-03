from flask import Blueprint
from app.api.projects.project_controller import ProjectController
# Importe apenas o que for realmente usado
from app.utils.auth_decorators import admin_required
from flask_login import login_required


project_bp = Blueprint("projects", __name__)

# Rota para buscar todos os projetos (GET - Read All)
@project_bp.route("/projects", methods=["GET"])
def get_all_projects():
    return ProjectController.get_all_projects()

# Rota para criar um novo projeto (POST - Create)
@project_bp.route("/projects", methods=["POST"])
@admin_required 
@login_required
def create_project():
    return ProjectController.create_project()

# Rota para buscar um projeto específico (GET - Read One)
@project_bp.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    # O ID é passado como argumento para a função
    return ProjectController.get_project(project_id)

# Rota para atualizar um projeto específico (PUT - Update)
@project_bp.route("/projects/<int:project_id>", methods=["PUT"])
@admin_required 
@login_required
def update_project(project_id):
    # O ID é passado como argumento para a função
    return ProjectController.update_project(project_id)

# Rota para deletar um projeto específico (DELETE - Delete)
@project_bp.route("/projects/<int:project_id>", methods=["DELETE"])
@admin_required 
@login_required
def delete_project(project_id):
    # O ID é passado como argumento para a função
    return ProjectController.delete_project(project_id)