# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from openai import OpenAI
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
# PLANIFICADOR IA
# =========================

@app.route("/api/planificar", methods=["POST"])
def planificar():

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

    return jsonify({
        "plan": texto
    })

# =========================

if __name__ == "__main__":
    app.run(debug=True)
