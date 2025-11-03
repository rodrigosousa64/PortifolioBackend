
from flask import Blueprint,render_template
import requests
import os
from dotenv import load_dotenv,find_dotenv
from pathlib import Path
from app.views.home import fhome_bp






load_dotenv(find_dotenv(filename=".env.local",usecwd=True))
API_URL = os.getenv("APIWEB")




@fhome_bp.route("/", methods=["GET"])
def home():
    print ("API_URL:", API_URL)  # Debug: Verifica o valor de API_URL
    projetos = []  # ✅ inicializa para evitar UnboundLocalError
    try:
        r = requests.get(f"{API_URL}/api/projects")
        r.raise_for_status()  # opcional: força erro para status != 200
        projetos = r.json()
    except Exception as e:
        print("Erro ao buscar projetos:", e)

    # renderiza o template com os dados
    return render_template("index.html", projetos=projetos)
