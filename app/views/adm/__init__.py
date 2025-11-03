from flask import Blueprint

admin_bp = Blueprint("admin", __name__, template_folder="templates",static_folder="static")



from app.views.adm import adm_routes