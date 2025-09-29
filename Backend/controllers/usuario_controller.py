# controllers/usuario_controller.py
from flask import jsonify, request
from models.usuario_models import Usuario
from infra.database import SessionLocal

class UsuarioController:

    @staticmethod
    def get_all_users():
        session = SessionLocal()
        try:
            usuarios = session.query(Usuario).all()
            return jsonify([u.as_dict() for u in usuarios]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def get_user(user_id):
        session = SessionLocal()
        try:
            usuario = session.query(Usuario).get(user_id)
            if usuario:
                return jsonify(usuario.as_dict()), 200
            return jsonify({"error": "User not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def create_user():
        session = SessionLocal()
        try:
            data = request.get_json()
            required_fields = ["name", "email", "password"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({"error": f"Field {field} is required"}), 400
            usuario = Usuario(**data)
            session.add(usuario)
            session.commit()
            session.refresh(usuario)
            return jsonify(usuario.as_dict()), 201
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def update_user(user_id):
        session = SessionLocal()
        try:
            data = request.get_json()
            usuario = session.query(Usuario).get(user_id)
            if not usuario:
                return jsonify({"error": "User not found"}), 404
            for key, value in data.items():
                if hasattr(usuario, key):
                    setattr(usuario, key, value)
            session.commit()
            session.refresh(usuario)
            return jsonify(usuario.as_dict()), 200
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def delete_user(user_id):
        session = SessionLocal()
        try:
            usuario = session.query(Usuario).get(user_id)
            if not usuario:
                return jsonify({"error": "User not found"}), 404
            session.delete(usuario)
            session.commit()
            return jsonify({"message": "User deleted successfully"}), 200
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()
