
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from curriculum import obtener_cursos, obtener_unidades, obtener_oa

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return render_template("app2.html")

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.json
        pregunta = data.get("pregunta")

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"Eres un experto pedagógico chileno."},
                {"role":"user","content":pregunta}
            ]
        )

        return jsonify({
            "respuesta":
            response.choices[0].message.content
        })

    except Exception as e:

        return jsonify({
            "respuesta":str(e)
        })

@app.route("/api/cursos/<asignatura>")
def api_cursos(asignatura):

    return jsonify(
        obtener_cursos(asignatura)
    )

@app.route("/api/unidades/<asignatura>/<curso>")
def api_unidades(asignatura, curso):

    return jsonify(
        obtener_unidades(asignatura, curso)
    )

@app.route("/api/oa/<asignatura>/<curso>/<unidad>")
def api_oa(asignatura, curso, unidad):

    return jsonify(
        obtener_oa(asignatura, curso, unidad)
    )

if __name__ == "__main__":
    app.run(debug=True)
