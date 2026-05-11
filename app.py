# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, send_file
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

import os
import json
from datetime import datetime

app = Flask(__name__)

# =========================
# OPENAI
# =========================

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# =========================
# BASE CURRICULAR AUTOMÁTICA
# =========================

BASE = {}

carpeta_data = "data"

for archivo in os.listdir(carpeta_data):

    if archivo.endswith(".json"):

        ruta = os.path.join(carpeta_data, archivo)

        with open(ruta, encoding="utf-8") as f:

            datos = json.load(f)

            nombre_asignatura = archivo.replace(".json", "")

            nombre_asignatura = nombre_asignatura.capitalize()

            BASE[nombre_asignatura] = datos

# =========================
# HISTORIAL
# =========================

historial = []

# =========================
# RUTAS
# =========================

@app.route("/")
def home():
    return render_template("app2.html")

@app.route("/api/base")
def base():
    return jsonify(BASE)

# =========================
# PLANIFICADOR IA
# =========================

@app.route("/api/planificar", methods=["POST"])
def planificar():

    try:

        data = request.json

        modulos = data.get("modulos", [])

        bloques = ""

        for m in modulos:
            bloques += f"- {m}\n"

        prompt = f"""
Eres un docente experto del sistema educativo chileno.

Genera contenido pedagógico profesional.

Asignatura:
{data['asignatura']}

Curso:
{data['curso']}

Unidad:
{data['unidad']}

Objetivos de Aprendizaje:
{chr(10).join(data['oa'])}

Debes generar solamente:

{bloques}

No agregues secciones no solicitadas.
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        texto = response.output[0].content[0].text

        historial.append({
            "fecha": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "plan": texto
        })

        return jsonify({
            "plan": texto
        })

    except Exception as e:

        return jsonify({
            "plan": f"ERROR IA: {str(e)}"
        })

# =========================
# CHAT IA DOCENTE
# =========================

@app.route("/api/chat", methods=["POST"])
def chat_ia():

    try:

        data = request.json

        pregunta = data.get("pregunta", "")

        prompt = f"""
Eres un asistente pedagógico experto del sistema educativo chileno.

Ayuda al docente de manera clara, profesional y práctica.

Pregunta:
{pregunta}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        texto = response.output[0].content[0].text

        return jsonify({
            "respuesta": texto
        })

    except Exception as e:

        return jsonify({
            "respuesta": f"ERROR IA: {str(e)}"
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

        for linea in texto.split("\\n"):

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
