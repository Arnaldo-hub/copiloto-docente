from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from openai import OpenAI

from curriculum import *

from planificador import *

import os

# =========================================
# APP
# =========================================

app = Flask(__name__)

# =========================================
# OPENAI
# =========================================

api_key = os.getenv(
    "OPENAI_API_KEY"
)

client = OpenAI(
    api_key=api_key
)

# =========================================
# HOME
# =========================================

@app.route("/")

def home():

    return render_template(
        "app2.html"
    )

# =========================================
# CHAT IA
# =========================================

@app.route(

    "/api/chat",

    methods=["POST"]

)

def api_chat():

    try:

        data = request.json

        pregunta = data.get(
            "pregunta"
        )

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[

                {
                    "role":"system",

                    "content":
                    "Eres un experto pedagógico chileno."
                },

                {
                    "role":"user",

                    "content":
                    pregunta
                }

            ]

        )

        texto = (

            response
            .choices[0]
            .message
            .content

        )

        return jsonify({

            "respuesta":
            texto

        })

    except Exception as e:

        return jsonify({

            "respuesta":
            str(e)

        })

# =========================================
# ASIGNATURAS
# =========================================

@app.route(
    "/api/asignaturas"
)

def api_asignaturas():

    try:

        asignaturas = obtener_asignaturas()

        return jsonify({

            "asignaturas":
            asignaturas

        })

    except Exception as e:

        return jsonify({

            "error":
            str(e)

        })

# =========================================
# CURSOS
# =========================================

@app.route(
    "/api/cursos/<asignatura>"
)

def api_cursos(asignatura):

    try:

        cursos = obtener_cursos(
            asignatura
        )

        return jsonify({

            "cursos":
            cursos

        })

    except Exception as e:

        return jsonify({

            "error":
            str(e)

        })

# =========================================
# UNIDADES
# =========================================

@app.route(
    "/api/unidades/<asignatura>/<curso>"
)

def api_unidades(

    asignatura,
    curso

):

    try:

        unidades = obtener_unidades(

            asignatura,
            curso

        )

        return jsonify({

            "unidades":
            unidades

        })

    except Exception as e:

        return jsonify({

            "error":
            str(e)

        })

# =========================================
# OA
# =========================================

@app.route(
    "/api/oa/<asignatura>/<curso>/<int:unidad>"
)

def api_oa(

    asignatura,
    curso,
    unidad

):

    try:

        oa = obtener_oa(

            asignatura,
            curso,
            unidad

        )

        return jsonify({

            "oa":
            oa

        })

    except Exception as e:

        return jsonify({

            "error":
            str(e)

        })

# =========================================
# PLANIFICADOR IA
# =========================================

@app.route(

    "/api/planificacion",

    methods=["POST"]

)

def api_planificacion():

    try:

        data = request.json

        asignatura = data.get(
            "asignatura"
        )

        curso = data.get(
            "curso"
        )

        unidad = data.get(
            "unidad"
        )

        oa = data.get(
            "oa"
        )

        resultado = generar_planificacion(

            asignatura,
            curso,
            unidad,
            oa

        )

        return jsonify({

            "resultado":
            resultado

        })

    except Exception as e:

        return jsonify({

            "resultado":
            str(e)

        })

# =========================================
# RUN
# =========================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )
