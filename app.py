# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import json
import os
from openai import OpenAI

app = Flask(__name__)

# =========================
# API KEY (DESDE RENDER)
# =========================
api_key = os.getenv("OPENAI_API_KEY")

print("API KEY OK:", True if api_key else False)

client = OpenAI(api_key=api_key)

# =========================
# BASE CURRICULAR
# =========================
BASE = {}
try:
    with open("base_curricular_oficial.json", encoding="utf-8") as f:
        BASE = json.load(f)
except Exception as e:
    print("ERROR BASE:", e)

# =========================
# USUARIOS
# =========================
os.makedirs("usuarios", exist_ok=True)
usuarios_file = "usuarios/usuarios.json"

if not os.path.exists(usuarios_file):
    with open(usuarios_file, "w", encoding="utf-8") as f:
        json.dump([], f)

def cargar_usuarios():
    try:
        with open(usuarios_file, encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def guardar_usuarios(data):
    with open(usuarios_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# =========================
# VISTAS
# =========================

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/app")
def app_page():
    return render_template("app.html")

# =========================
# LOGIN / REGISTRO
# =========================

@app.route("/api/registro", methods=["POST"])
def registro():
    data = request.json or {}
    usuario = data.get("usuario", "")
    password = data.get("password", "")

    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario:
            return jsonify({"ok": False, "msg": "Usuario ya existe"})

    usuarios.append({"usuario": usuario, "password": password})
    guardar_usuarios(usuarios)

    return jsonify({"ok": True})

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    usuario = data.get("usuario", "")
    password = data.get("password", "")

    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario and u["password"] == password:
            return jsonify({"ok": True})

    return jsonify({"ok": False})

# =========================
# BASE
# =========================

@app.route("/api/base")
def base():
    return jsonify(BASE)

# =========================
# IA (FUNCIONANDO BIEN)
# =========================

@app.route("/api/planificar", methods=["POST"])
def planificar():
    try:
        if not api_key:
            return jsonify({"plan": "❌ Falta OPENAI_API_KEY en Render"})

        data = request.json or {}

        asignatura = data.get("asignatura", "")
        curso = data.get("curso", "")
        unidad = data.get("unidad", "")
        oa = data.get("oa", [])

        if not oa:
            return jsonify({"plan": "Selecciona al menos un OA"})

        prompt = f"""
Genera una planificación de clase profesional.

Asignatura: {asignatura}
Curso: {curso}
Unidad: {unidad}

Objetivos:
{chr(10).join(oa)}

Incluye:
- Objetivo
- Inicio
- Desarrollo
- Cierre
- Evaluación
- Recursos
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        texto = response.output[0].content[0].text

        return jsonify({"plan": texto})

    except Exception as e:
        print("ERROR IA:", e)
        return jsonify({"plan": f"Error IA: {str(e)}"})

# =========================

if __name__ == "__main__":
    app.run()
