from flask import Blueprint, jsonify
from app.controllers.migrations_controller import migrations_controller


migrations_bp = Blueprint("migrations", __name__)   
"""
migrations_bp.route("/migrations/upgrade", methods=["GET"])(migrations_controller.upgrade_db)"""
