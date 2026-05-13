from flask import Flask, render_template, request, jsonify

from curriculum import (
    obtener_unidades,
    obtener_oa
)

from pedagogia import (

    generar_objetivos,
    generar_indicadores,
    generar_habilidades,
    generar_actitudes,
    generar_nee,
    generar_evaluacion

)

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
# PEDAGOGIA
# =========================================

@app.route("/api/pedagogia", methods=["POST"])
def api_pedagogia():

    data = request.json

    asignatura = data.get("asignatura")
    curso = data.get("curso")
    unidad = data.get("unidad")
    oa = data.get("oa")

    resultado = f"""

📚 ASIGNATURA:
{asignatura}

🎓 CURSO:
{curso}

📖 UNIDAD:
{unidad}

🎯 OA:
{oa}

"""

    # =====================================
    # OBJETIVOS
    # =====================================

    if data.get("objetivos"):

        resultado += "\n\n🎯 OBJETIVOS\n"

        objetivos = generar_objetivos(
            asignatura,
            curso,
            unidad,
            oa
        )

        for item in objetivos:

            resultado += f"\n• {item}"

    # =====================================
    # INDICADORES
    # =====================================

    if data.get("indicadores"):

        resultado += "\n\n📊 INDICADORES\n"

        indicadores = generar_indicadores(
            asignatura,
            curso,
            unidad,
            oa
        )

        for item in indicadores:

            resultado += f"\n• {item}"

    # =====================================
    # HABILIDADES
    # =====================================

    if data.get("habilidades"):

        resultado += "\n\n🧠 HABILIDADES\n"

        habilidades = generar_habilidades(
            asignatura,
            curso,
            unidad,
            oa
        )

        for item in habilidades:

            resultado += f"\n• {item}"

    # =====================================
    # ACTITUDES
    # =====================================

    if data.get("actitudes"):

        resultado += "\n\n🤝 ACTITUDES\n"

        actitudes = generar_actitudes(
            asignatura,
            curso,
            unidad,
            oa
        )

        for item in actitudes:

            resultado += f"\n• {item}"

    # =====================================
    # NEE
    # =====================================

    if data.get("nee"):

        resultado += "\n\n♿ ADAPTACIONES NEE\n"

        nee = generar_nee(
            asignatura,
            curso,
            unidad,
            oa
        )

        for item in nee:

            resultado += f"\n• {item}"

    # =====================================
    # EVALUACION
    # =====================================

    if data.get("evaluacion"):

        resultado += "\n\n📝 EVALUACIÓN\n"

        evaluacion = generar_evaluacion(
            asignatura,
            curso,
            unidad,
            oa
        )

        for item in evaluacion:

            resultado += f"\n• {item}"

    return jsonify({

        "resultado": resultado

    })

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    app.run(debug=True)
