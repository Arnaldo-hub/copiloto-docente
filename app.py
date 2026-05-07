# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from openai import OpenAI

app = Flask(__name__)

# =========================
# API KEY DESDE RENDER
# =========================
api_key = os.getenv("OPENAI_API_KEY")
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

    usuarios.append({
        "usuario": usuario,
        "password": password,
        "historial": []
    })

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
            return jsonify({"ok": True, "usuario": usuario})

    return jsonify({"ok": False})

# =========================
# BASE
# =========================

@app.route("/api/base")
def base():
    return jsonify(BASE)

# =========================
# GUARDAR HISTORIAL
# =========================

def guardar_plan(usuario, plan):
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario:
            u["historial"].append({
                "fecha": datetime.now().strftime("%d-%m-%Y %H:%M"),
                "plan": plan
            })

    guardar_usuarios(usuarios)

# =========================
# OBTENER HISTORIAL
# =========================

@app.route("/api/historial", methods=["POST"])
def historial():
    data = request.json or {}
    usuario = data.get("usuario")

    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario:
            return jsonify(u.get("historial", []))

    return jsonify([])

# =========================
# IA + GUARDADO
# =========================

@app.route("/api/planificar", methods=["POST"])
def planificar():
    try:
        if not api_key:
            return jsonify({"plan": "❌ Falta OPENAI_API_KEY en Render"})

        data = request.json or {}
        usuario = data.get("usuario", "")

        prompt = f"""
Eres un docente experto del sistema educativo chileno.

Genera una planificación de clase profesional clara, estructurada y lista para usar en aula.

Incluye:
- Objetivo de la clase
- Inicio (motivación)
- Desarrollo (actividades detalladas)
- Cierre
- Evaluación (formativa y/o sumativa)
- Recursos
- Adaptaciones (NEE)

Datos:
Asignatura: {data.get('asignatura','')}
Curso: {data.get('curso','')}
Unidad: {data.get('unidad','')}

OA:
{chr(10).join(data.get('oa', []))}
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        texto = response.output[0].content[0].text

        # Guardar en historial
        if usuario:
            guardar_plan(usuario, texto)

        return jsonify({"plan": texto})

    except Exception as e:
        print("ERROR IA:", e)
        return jsonify({"plan": f"Error IA: {str(e)}"})

# =========================

if __name__ == "__main__":
    app.run()
