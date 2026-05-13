from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from curriculum import *
from planificador import *
import os

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return render_template("app2.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():

    try:

        data = request.json
        pregunta = data.get("pregunta")

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[

                {
                    "role":"system",
                    "content":"Eres un experto pedagógico chileno."
                },

                {
                    "role":"user",
                    "content":pregunta
                }

            ]

        )

        texto = response.choices[0].message.content

        return jsonify({
            "respuesta":texto
        })

    except Exception as e:

        return jsonify({
            "respuesta":str(e)
        })

@app.route("/api/cursos/<asignatura>")
def api_cursos(asignatura):

    return jsonify({
        "cursos":obtener_cursos(asignatura)
    })

@app.route("/api/unidades/<asignatura>/<curso>")
def api_unidades(asignatura, curso):

    return jsonify({
        "unidades":obtener_unidades(
            asignatura,
            curso
        )
    })

@app.route("/api/oa/<asignatura>/<curso>/<int:unidad>")
def api_oa(asignatura, curso, unidad):

    return jsonify({
        "oa":obtener_oa(
            asignatura,
            curso,
            unidad
        )
    })

@app.route("/api/planificacion", methods=["POST"])
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
            "resultado":resultado
        })

    except Exception as e:

        return jsonify({
            "resultado":str(e)
        })

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
