from flask import Blueprint
from controllers.project_controller import ProjectController

project_bp = Blueprint("projects", __name__)

project_bp.route("/projects", methods=["GET"])(ProjectController.get_all_projects)
project_bp.route("/projects/<int:project_id>", methods=["GET"])(ProjectController.get_project)
project_bp.route("/projects", methods=["POST"])(ProjectController.create_project)
project_bp.route("/projects/<int:project_id>", methods=["PUT"])(ProjectController.update_project)
project_bp.route("/projects/<int:project_id>", methods=["DELETE"])(ProjectController.delete_project)
