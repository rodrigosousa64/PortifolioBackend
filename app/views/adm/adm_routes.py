from flask import Blueprint, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from app.views.adm import admin_bp





load_dotenv(find_dotenv(filename=".env.local",usecwd=True))
API_URL = os.getenv("APIWEB")


# Lista de projetos
@admin_bp.route("/projects", methods=["GET"])
def projects_list():
    projetos = []
    try:
        r = requests.get(f"{API_URL}/api/projects")
        r.raise_for_status()
        projetos = r.json()
    except Exception as e:
        print("Erro ao buscar projetos:", e)
    return render_template("projects_list.html", projects=projetos)

# Formulário para criar projeto
@admin_bp.route("/projects/new", methods=["GET"])
def project_new():
    return render_template("project_form.html")

# Criar projeto
@admin_bp.route("/projects", methods=["POST"])
def project_create():
    data = {
        "name": request.form.get("name"),
        "description": request.form.get("description"),
        "technologies": request.form.get("technologies") or "",
        "git_link": request.form.get("git_link") or "",
        "hosted_link": request.form.get("hosted_link") or "",
        "image_url": request.form.get("image_url") or ""
    }
    try:
        r = requests.post(f"{API_URL}/api/projects", json=data)
        r.raise_for_status()
    except Exception as e:
        print("Erro ao criar projeto:", e)
    return redirect(url_for("admin.projects_list"))

# Deletar projeto
@admin_bp.route("/projects/<int:project_id>/delete", methods=["POST"])
def project_delete(project_id):
    try:
        r = requests.delete(f"{API_URL}/api/projects/{project_id}")
        r.raise_for_status()
    except Exception as e:
        print("Erro ao deletar projeto:", e)
    return redirect(url_for("admin.projects_list"))



# rotas para editar usuário


@admin_bp.route("/projects/<int:project_id>/edit", methods=["GET"])
def usuario_edit(usuario_id):
    projeto = {}
    try:
        r = requests.get(f"{API_URL}/api/projects/{project_id}")
        r.raise_for_status()
        projeto = r.json()
    except Exception as e:
        print("Erro ao buscar projeto:", e)
    return render_template("project_edit_form.html", project=projeto)
