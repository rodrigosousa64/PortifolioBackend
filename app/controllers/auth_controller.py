from flask import jsonify, request, session
from app.models.usuario_models import Usuario
from app.infra.database import SessionLocal
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

class AuthController:

    @staticmethod
    def register_user():
        db_session = SessionLocal()
        try:
            data = request.get_json()
            required_fields = ["name", "email", "password"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({"error": f"Field {field} is required"}), 400

            # evita duplicidade
            if db_session.query(Usuario).filter_by(email=data["email"]).first():
                return jsonify({"error": "Email already registered"}), 400

            user = Usuario(
                name=data["name"],
                email=data["email"],
            )
            user.set_password(data["password"])  # hash da senha
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)

            return jsonify(user.as_dict()), 201
        except Exception as e:
            db_session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            db_session.close()

    @staticmethod
    def login_user():
        db_session = SessionLocal()
        try:
            data = request.get_json()
            if not data.get("email") or not data.get("password"):
                return jsonify({"error": "Email and password are required"}), 400

            user = db_session.query(Usuario).filter_by(email=data["email"]).first()
            if not user or not user.check_password(data["password"]):
                return jsonify({"error": "Invalid credentials"}), 401

            login_user(user)  # flask-login
            session["user_id"] = user.id  # opcional para rastrear
            return jsonify({"message": "Login successful", "user": user.as_dict()}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            db_session.close()

    @staticmethod
    def logout_user():
        try:
            logout_user()
            session.clear()
            return jsonify({"message": "Logged out successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
