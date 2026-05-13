from flask import Flask, render_template, request, jsonify
from curriculum import obtener_unidades, obtener_oa

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("app2.html")

@app.route("/api/unidades", methods=["POST"])
def api_unidades():
    data = request.json
    unidades = obtener_unidades(
        data["asignatura"],
        data["curso"]
    )
    return jsonify(unidades)

@app.route("/api/oa", methods=["POST"])
def api_oa():
    data = request.json
    oa = obtener_oa(
        data["asignatura"],
        data["curso"],
        data["unidad"]
    )
    return jsonify(oa)

@app.route("/api/pedagogia", methods=["POST"])
def api_pedagogia():
    data = request.json

    return jsonify({
        "resultado": f'''
Asignatura: {data.get("asignatura")}
Curso: {data.get("curso")}
Unidad: {data.get("unidad")}
OA: {data.get("oa")}

Planificación generada correctamente.
'''
    })

if __name__ == "__main__":
    app.run(debug=True)
