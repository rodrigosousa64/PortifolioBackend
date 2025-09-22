from flask import Blueprint, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os

health_bp = Blueprint("health", __name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mydb")
engine = create_engine(DATABASE_URL)


@health_bp.route("/health", methods=["GET"])
def health_check():
    health_info = {"status": "healthy", "db": "unknown", "connections": None}
    
    try:
        # Tenta conectar e executar uma query simples
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            
            # Contar quantas conexões estão ativas
            result = connection.execute(text("SELECT COUNT(*) FROM pg_stat_activity"))
            health_info["connections"] = result.scalar()
            health_info["db"] = "connected"
            
    except OperationalError:
        health_info["status"] = "unhealthy"
        health_info["db"] = "cannot connect"
    
    return jsonify(health_info), 200 if health_info["status"] == "healthy" else 500