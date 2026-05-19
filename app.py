from flask import Flask, render_template, request, jsonify

from curriculum import (
    obtener_cursos,
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

# =========================================
# APP
# =========================================

app = Flask(__name__)

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template(
        "app2.html"
    )

# =========================================
# CURSOS
# =========================================

@app.route(
    "/api/cursos/<asignatura>"
)
def api_cursos(asignatura):

    cursos = obtener_cursos(
        asignatura
    )

    return jsonify({

        "cursos": cursos

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

    unidades = obtener_unidades(

        asignatura,
        curso

    )

    return jsonify({

        "unidades": unidades

    })

# =========================================
# OA
# =========================================

@app.route(
    "/api/oa/<asignatura>/<curso>/<unidad>"
)
def api_oa(

    asignatura,
    curso,
    unidad

):

    oa = obtener_oa(

        asignatura,
        curso,
        unidad

    )

    return jsonify({

        "oa": oa

    })

# =========================================
# PEDAGOGÍA IA
# =========================================

@app.route(
    "/api/pedagogia",
    methods=["POST"]
)
def api_pedagogia():

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
    # EVALUACIÓN
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

    app.run(
        debug=True
    )
