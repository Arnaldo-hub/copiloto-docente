# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import json
import os

app = Flask(__name__)

# =========================
# OPENAI
# =========================

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# =========================
# BASE CURRICULAR
# =========================

with open("base_curricular_oficial.json", encoding="utf-8") as f:
    BASE = json.load(f)

# =========================
# RUTAS HTML
# =========================

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/app")
def app_page():
    return render_template("app2.html")

# =========================
# API BASE
# =========================

@app.route("/api/base")
def base():
    return jsonify(BASE)

# =========================
# LOGIN SIMPLE
# =========================

@app.route("/api/login", methods=["POST"])
def login():

    data = request.json

    return jsonify({
        "ok": True,
        "usuario": data["usuario"]
    })

# =========================
# HISTORIAL TEMPORAL
# =========================

historial = []

# =========================
# PLANIFICADOR IA
# =========================

@app.route("/api/planificar", methods=["POST"])
def planificar():

    try:

        data = request.json

        prompt = f"""
Genera una planificación de clase profesional para Chile.

Asignatura:
{data['asignatura']}

Curso:
{data['curso']}

Unidad:
{data['unidad']}

OA:
{chr(10).join(data['oa'])}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        texto = response.output[0].content[0].text

        historial.append(texto)

        return jsonify({
            "plan": texto
        })

    except Exception as e:

        return jsonify({
            "plan": f"ERROR IA: {str(e)}"
        })

# =========================
# HISTORIAL
# =========================

@app.route("/api/historial", methods=["POST"])
def ver_historial():

    return jsonify(historial)

# =========================
# PDF
# =========================

@app.route("/api/pdf", methods=["POST"])
def generar_pdf():

    try:

        data = request.json

        texto = data.get("plan", "")

        archivo = "planificacion.pdf"

        doc = SimpleDocTemplate(archivo)

        styles = getSampleStyleSheet()

        contenido = []

        for linea in texto.split("\n"):

            contenido.append(
                Paragraph(linea, styles["Normal"])
            )

            contenido.append(
                Spacer(1, 10)
            )

        doc.build(contenido)

        return send_file(
            archivo,
            as_attachment=True
        )

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================

if __name__ == "__main__":
    app.run(debug=True)
