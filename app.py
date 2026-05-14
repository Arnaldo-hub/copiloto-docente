from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import session
from flask import redirect
from flask import url_for

from openai import OpenAI

from curriculum import *
from planificador import *

import os
import json

# =========================================
# APP
# =========================================

app = Flask(__name__)

app.secret_key = "copiloto_docente_secret"

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
# USUARIOS
# =========================================

RUTA_USUARIOS = os.path.join(
    "usuarios",
    "usuarios.json"
)

def leer_usuarios():

    with open(
        RUTA_USUARIOS,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)

# =========================================
# LOGIN
# =========================================

@app.route("/login")
def login_page():

    return render_template(
        "login.html"
    )

@app.route(
    "/api/login",
    methods=["POST"]
)
def api_login():

    data = request.json

    usuario = data.get(
        "usuario"
    )

    password = data.get(
        "password"
    )

    usuarios = leer_usuarios()

    for u in usuarios:

        if (

            u["usuario"] == usuario

            and

            u["password"] == password

        ):

            session["usuario"] = usuario

            session["nombre"] = u["nombre"]

            return jsonify({

                "success":True

            })

    return jsonify({

        "success":False

    })

# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login_page")
    )

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    if "usuario" not in session:

        return redirect(
            url_for("login_page")
        )

    return render_template(
        "app2.html",
        nombre=session.get("nombre")
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

            "respuesta":texto

        })

    except Exception as e:

        return jsonify({

            "respuesta":str(e)

        })

# =========================================
# CURSOS
# =========================================

@app.route(
    "/api/cursos/<asignatura>"
)
def api_cursos(asignatura):

    return jsonify({

        "cursos":
        obtener_cursos(asignatura)

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

    return jsonify({

        "unidades":

        obtener_unidades(
            asignatura,
            curso
        )

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

    return jsonify({

        "oa":

        obtener_oa(
            asignatura,
            curso,
            unidad
        )

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

        opciones = {

            "objetivos":
            data.get("objetivos"),

            "indicadores":
            data.get("indicadores"),

            "habilidades":
            data.get("habilidades"),

            "actitudes":
            data.get("actitudes"),

            "evaluacion":
            data.get("evaluacion"),

            "nee":
            data.get("nee"),

            "recursos":
            data.get("recursos")

        }

        resultado = generar_planificacion(

            data.get("asignatura"),

            data.get("curso"),

            data.get("unidad"),

            data.get("oa"),

            opciones

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
