# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, send_file
import json
import os
from datetime import datetime
from openai import OpenAI

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# API KEY
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# BASE
with open("base_curricular_oficial.json", encoding="utf-8") as f:
    BASE = json.load(f)

# USUARIOS
os.makedirs("usuarios", exist_ok=True)
usuarios_file = "usuarios/usuarios.json"

if not os.path.exists(usuarios_file):
    with open(usuarios_file, "w", encoding="utf-8") as f:
        json.dump([], f)

def cargar_usuarios():
    with open(usuarios_file, encoding="utf-8") as f:
        return json.load(f)

def guardar_usuarios(data):
    with open(usuarios_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# VISTAS
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/app")
def app_page():
    return render_template("app.html")

# LOGIN
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == data["usuario"] and u["password"] == data["password"]:
            return jsonify({"ok": True, "usuario": u["usuario"]})

    return jsonify({"ok": False})

# REGISTRO
@app.route("/api/registro", methods=["POST"])
def registro():
    data = request.json
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == data["usuario"]:
            return jsonify({"ok": False})

    usuarios.append({
        "usuario": data["usuario"],
        "password": data["password"],
        "historial": []
    })

    guardar_usuarios(usuarios)
    return jsonify({"ok": True})

# BASE
@app.route("/api/base")
def base():
    return jsonify(BASE)

# GUARDAR HISTORIAL
def guardar_plan(usuario, plan):
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario:
            u["historial"].append({
                "fecha": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "plan": plan
            })

    guardar_usuarios(usuarios)

# HISTORIAL
@app.route("/api/historial", methods=["POST"])
def historial():
    data = request.json
    usuario = data.get("usuario")

    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario:
            return jsonify(u["historial"])

    return jsonify([])

# IA
@app.route("/api/planificar", methods=["POST"])
def planificar():
    data = request.json
    usuario = data.get("usuario", "")

    prompt = f"""
Eres un docente experto del sistema educativo chileno.

Genera una planificación profesional.

Asignatura: {data['asignatura']}
Curso: {data['curso']}
Unidad: {data['unidad']}

OA:
{chr(10).join(data['oa'])}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    texto = response.output[0].content[0].text

    guardar_plan(usuario, texto)

    return jsonify({"plan": texto})

# PDF REAL DESCARGABLE
@app.route("/api/pdf", methods=["POST"])
def generar_pdf():
    data = request.json
    texto = data.get("plan", "")

    filename = "planificacion.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    for linea in texto.split("\n"):
        content.append(Paragraph(linea, styles["Normal"]))
        content.append(Spacer(1, 10))

    doc.build(content)

    return send_file(filename, as_attachment=True)

# RUN
if __name__ == "__main__":
    app.run()
