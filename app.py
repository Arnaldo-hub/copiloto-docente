from flask import Flask, render_template, request, jsonify

from openai import OpenAI

from curriculum import (
    obtener_unidades,
    obtener_oa
)

import os

# =========================================
# OPENAI
# =========================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================================
# APP
# =========================================

app = Flask(__name__)

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template("app2.html")

# =========================================
# UNIDADES
# =========================================

@app.route("/api/unidades", methods=["POST"])
def api_unidades():

    data = request.json

    unidades = obtener_unidades(

        data["asignatura"],
        data["curso"]

    )

    return jsonify(unidades)

# =========================================
# OA
# =========================================

@app.route("/api/oa", methods=["POST"])
def api_oa():

    data = request.json

    oa = obtener_oa(

        data["asignatura"],
        data["curso"],
        data["unidad"]

    )

    return jsonify(oa)

# =========================================
# PEDAGOGIA IA REAL
# =========================================

@app.route("/api/pedagogia", methods=["POST"])
def api_pedagogia():

    data = request.json

    asignatura = data.get("asignatura")
    curso = data.get("curso")
    unidad = data.get("unidad")
    oa = data.get("oa")

    bloques = []

    if data.get("objetivos"):
        bloques.append("objetivos de aprendizaje")

    if data.get("indicadores"):
        bloques.append("indicadores de evaluación")

    if data.get("habilidades"):
        bloques.append("habilidades")

    if data.get("actitudes"):
        bloques.append("actitudes")

    if data.get("nee"):
        bloques.append("adaptaciones NEE")

    if data.get("evaluacion"):
        bloques.append("evaluación")

    bloques_texto = ", ".join(bloques)

    prompt = f"""

Eres un experto en educación chilena y planificación curricular.

Genera una planificación pedagógica profesional.

ASIGNATURA:
{asignatura}

CURSO:
{curso}

UNIDAD:
{unidad}

OA:
{oa}

Debes generar:

{bloques_texto}

La respuesta debe:

- ser extensa
- profesional
- clara
- usable por docentes reales
- alineada al currículum chileno
- incluir estrategias pedagógicas
- incluir ejemplos concretos
- incluir metodologías activas

"""

    try:

        respuesta = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content": "Eres un experto pedagógico chileno."
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.7

        )

        texto = respuesta.choices[0].message.content

        return jsonify({

            "resultado": texto

        })

    except Exception as e:

        return jsonify({

            "resultado":
            f"ERROR IA:\n\n{str(e)}"

        })

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    app.run(debug=True)
