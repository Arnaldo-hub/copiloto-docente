from flask import Flask, render_template, request, jsonify
import json
import os
import datetime

from openai import OpenAI

app = Flask(__name__)

# =========================
# OPENAI
# =========================
client = OpenAI(api_key=os.environ.get("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
"))

# =========================
# BASE CURRICULAR
# =========================
BASE = {}

try:
    with open("base_curricular_oficial.json", encoding="utf-8") as f:
        BASE = json.load(f)
except Exception as e:
    print("ERROR JSON:", e)

# =========================
# USUARIOS
# =========================
usuarios_file = "usuarios/usuarios.json"

if not os.path.exists(usuarios_file):
    with open(usuarios_file, "w") as f:
        json.dump([], f)

# =========================
# RUTAS
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/base")
def base():
    return jsonify(BASE)


# =========================
# LOGIN
# =========================

@app.route("/api/registro", methods=["POST"])
def registro():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    with open(usuarios_file, encoding="utf-8") as f:
        usuarios = json.load(f)

    for u in usuarios:
        if u["usuario"] == usuario:
            return jsonify({"ok": False, "msg": "Usuario ya existe"})

    usuarios.append({"usuario": usuario, "password": password})

    with open(usuarios_file, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2)

    return jsonify({"ok": True})


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    usuario = data.get("usuario")
    password = data.get("password")

    with open(usuarios_file, encoding="utf-8") as f:
        usuarios = json.load(f)

    for u in usuarios:
        if u["usuario"] == usuario and u["password"] == password:
            return jsonify({"ok": True})

    return jsonify({"ok": False})


# =========================
# PLANIFICACIÓN IA + GUARDADO
# =========================

@app.route("/api/planificar", methods=["POST"])
def planificar():
    try:
        data = request.json

        asignatura = data.get("asignatura", "")
        curso = data.get("curso", "")
        unidad = data.get("unidad", "")
        oa_lista = data.get("oa", [])

        prompt = f"""
Genera una planificación de clase profesional.

Asignatura: {asignatura}
Curso: {curso}
Unidad: {unidad}

Objetivos:
{chr(10).join(oa_lista)}

Incluye:
- Objetivo
- Inicio
- Desarrollo
- Cierre
- Evaluación
- Recursos
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        plan = response.choices[0].message.content

        # GUARDAR
        os.makedirs("historial", exist_ok=True)

        nombre = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ruta = f"historial/plan_{nombre}.json"

        with open(ruta, "w", encoding="utf-8") as f:
            json.dump({
                "asignatura": asignatura,
                "curso": curso,
                "unidad": unidad,
                "oa": oa_lista,
                "plan": plan
            }, f, ensure_ascii=False, indent=2)

        return jsonify({"plan": plan})

    except Exception as e:
        print("ERROR IA:", e)
        return jsonify({"plan": "? Error IA"})


# =========================
# HISTORIAL
# =========================

@app.route("/api/historial")
def historial():
    try:
        archivos = os.listdir("historial")
        data = []

        for archivo in archivos:
            with open(f"historial/{archivo}", encoding="utf-8") as f:
                data.append(json.load(f))

        return jsonify(data)

    except:
        return jsonify([])


# =========================
if __name__ == "__main__":
    app.run()