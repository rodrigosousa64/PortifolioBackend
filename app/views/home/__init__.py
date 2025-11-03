from flask import Blueprint


fhome_bp = Blueprint("fhome", __name__)


from app.views.home import home_routes