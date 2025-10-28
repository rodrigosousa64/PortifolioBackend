# controllers/usuario_controller.py
from flask import jsonify, request
from app.models.usuario_models import Usuario
from app.infra.database import SessionLocal

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
        
        # 1. Validação dos campos necessários, AGORA INCLUINDO 'is_admin'
        required_fields = ["name", "email", "password", "is_admin"]
        
        for field in required_fields:
            # 1a. Verifica se a chave existe
            if field not in data:
                return jsonify({"error": f"Field '{field}' is required"}), 400
            
            # 1b. Validação específica para 'is_admin' (deve ser booleano)
            if field == "is_admin":
                if not isinstance(data[field], bool):
                    return jsonify({"error": "Field 'is_admin' must be a boolean (true or false)"}), 400
            
            # 1c. Validação para os outros campos (não podem ser vazios)
            elif not data[field]: 
                 return jsonify({"error": f"Field '{field}' cannot be empty"}), 400

        
        # 2. Extrai a senha Pura
        raw_password = data.pop("password") 
        
        # 3. Cria o objeto Usuario com TODOS os dados do JSON (name, email, is_admin)
        # O valor de 'is_admin' virá DIRETAMENTE do 'data'
        usuario = Usuario(**data)
        
        # 4. Chama o método de segurança para gerar o hash
        usuario.set_password(raw_password)
        
        # 5. Persistência no banco
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        
        # 6. Retorno de Sucesso
        # Se o usuário enviou 'is_admin: true', o usuário criado será admin.
        # Se enviou 'is_admin: false', não será.
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
