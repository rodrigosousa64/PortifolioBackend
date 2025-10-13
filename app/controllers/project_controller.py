from flask import jsonify, request
from app.models.projects_models import Project
from app.infra.database import SessionLocal

class ProjectController:

    @staticmethod
    def get_all_projects():
        session = SessionLocal()
        try:
            projects = session.query(Project).all()
            return jsonify([p.as_dict() for p in projects]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def get_project(project_id):
        session = SessionLocal()
        try:
            project = session.query(Project).get(project_id)
            if project:
                return jsonify(project.as_dict()), 200
            return jsonify({"error": "Project not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def create_project():
        session = SessionLocal()
        try:
            data = request.get_json()
            required_fields = ["name", "technologies", "description"]
            for field in required_fields:
                if field not in data or not data[field]:
                    return jsonify({"error": f"Field {field} is required"}), 400
            project = Project(**data)
            session.add(project)
            session.commit()
            session.refresh(project)
            return jsonify(project.as_dict()), 201
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def update_project(project_id):
        session = SessionLocal()
        try:
            data = request.get_json()
            project = session.query(Project).get(project_id)
            if not project:
                return jsonify({"error": "Project not found"}), 404
            for key, value in data.items():
                if hasattr(project, key):
                    setattr(project, key, value)
            session.commit()
            session.refresh(project)
            return jsonify(project.as_dict()), 200
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()

    @staticmethod
    def delete_project(project_id):
        session = SessionLocal()
        try:
            project = session.query(Project).get(project_id)
            if not project:
                return jsonify({"error": "Project not found"}), 404
            session.delete(project)
            session.commit()
            return jsonify({"message": "Project deleted successfully"}), 200
        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()
