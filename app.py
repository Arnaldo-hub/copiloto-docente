from flask import Flask, render_template, request, jsonify

from curriculum import (
    obtener_cursos,
    obtener_unidades,
    obtener_oa
)

from pedagogia import (
    generar_respuesta,
    generar_objetivos,
    generar_indicadores,
    generar_habilidades,
    generar_actitudes,
    generar_nee,
    generar_evaluacion
)

from auth import auth

# =========================================
# APP
# =========================================

app = Flask(__name__)
app.secret_key = "aulamind_secret_2026"

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

    try:

        cursos = obtener_cursos(
            asignatura
        )

        return jsonify({

            "cursos": cursos

        })

    except Exception as e:

        print("ERROR CURSOS:", e)

        return jsonify({

            "cursos": []

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

            "unidades": unidades

        })

    except Exception as e:

        print("ERROR UNIDADES:", e)

        return jsonify({

            "unidades": []

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

    try:

        oa = obtener_oa(

            asignatura,
            curso,
            unidad

        )

        return jsonify({

            "oa": oa

        })

    except Exception as e:

        print("ERROR OA:", e)

        return jsonify({

            "oa": []

        })

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
            "pregunta",
            ""
        )

        respuesta = generar_respuesta(
            pregunta
        )

        return jsonify({

            "respuesta": respuesta

        })

    except Exception as e:

        print("ERROR CHAT:", e)

        return jsonify({

            "respuesta": f"""

# ❌ Error

No fue posible responder.

Detalle:
{str(e)}

"""

        })

# =========================================
# PEDAGOGÍA IA
# =========================================

@app.route(
    "/api/pedagogia",
    methods=["POST"]
)
def api_pedagogia():

    try:

        data = request.json

        asignatura = data.get(
            "asignatura",
            ""
        )

        curso = data.get(
            "curso",
            ""
        )

        unidad = data.get(
            "unidad",
            ""
        )

        oa = data.get(
            "oa",
            ""
        )

        resultado = f"""

# ✅ Planificación Generada

---

## 📚 Contexto Pedagógico

### 📘 Asignatura
{asignatura}

### 🎓 Curso
{curso}

### 📖 Unidad
{unidad}

### 🎯 OA
{oa}

---

"""

        # =====================================
        # OBJETIVOS
        # =====================================

        if data.get("objetivos"):

            resultado += """

# 🎯 Objetivos

"""

            resultado += generar_objetivos(

                asignatura,
                curso,
                unidad,
                oa

            )

        # =====================================
        # INDICADORES
        # =====================================

        if data.get("indicadores"):

            resultado += """

# 📊 Indicadores

"""

            resultado += generar_indicadores(

                asignatura,
                curso,
                unidad,
                oa

            )

        # =====================================
        # HABILIDADES
        # =====================================

        if data.get("habilidades"):

            resultado += """

# 🧠 Habilidades

"""

            resultado += generar_habilidades(

                asignatura,
                curso,
                unidad,
                oa

            )

        # =====================================
        # ACTITUDES
        # =====================================

        if data.get("actitudes"):

            resultado += """

# 🤝 Actitudes

"""

            resultado += generar_actitudes(

                asignatura,
                curso,
                unidad,
                oa

            )

        # =====================================
        # NEE
        # =====================================

        if data.get("nee"):

            resultado += """

# ♿ Adaptaciones NEE

"""

            resultado += generar_nee(

                asignatura,
                curso,
                unidad,
                oa

            )

        # =====================================
        # EVALUACIÓN
        # =====================================

        if data.get("evaluacion"):

            resultado += """

# 📝 Evaluación

"""

            resultado += generar_evaluacion(

                asignatura,
                curso,
                unidad,
                oa

            )

        return jsonify({

            "resultado": resultado

        })

    except Exception as e:

        print("ERROR PEDAGOGIA:", e)

        return jsonify({

            "resultado": f"""

# ❌ Error

No fue posible generar la planificación.

## Detalle técnico

{str(e)}

"""

        })

# =========================================
# MAIN
# =========================================

app.register_blueprint(auth)
if __name__ == "__main__":

    app.run(

        host="0.0.0.0",
        port=10000,
        debug=True

    )
