import subprocess
from flask import jsonify   





class migrations_controller:
     
     @staticmethod
     def upgrade_db():
        try:
            subprocess.run(
            ["flask", "db", "migrate", "-m", "initial", "--directory", "infra/migrations"],
            check=True
        )
            subprocess.run(
            ["flask", "db", "upgrade", "--directory", "infra/migrations"],
            check=True
        )
            return jsonify({"status": "success", "message": "Migrations appliedd"})
        except subprocess.CalledProcessError as e:
            return jsonify({"status": "error", "message": str(e)})
           
