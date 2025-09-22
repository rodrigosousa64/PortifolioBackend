
from flask import Blueprint
from controllers.project_controller import ProjectController
home_bp = Blueprint("home", __name__, template_folder="templates", static_folder='static',static_url_path='/home_static' )


@home_bp.route("/", methods=["GET"])
def home():
    return ProjectController.get_all_projects()