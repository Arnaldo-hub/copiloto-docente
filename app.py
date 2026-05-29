from flask import Flask, render_template, request, jsonify
from flask import session
from flask import redirect

from database import (
    conectar_db,
    crear_tablas,
    db,
    Usuario,
    Historial
)

from curriculum import (

    obtener_cursos,
    obtener_unidades,
    obtener_oa,
    obtener_oa_completo

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
from imagen import generar_imagen

# =========================================
# APP
# =========================================

app = Flask(__name__)
app.secret_key = "aulamind_secret_2026"
conectar_db(app)

crear_tablas(app)

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    return render_template(
        "app2.html"
    )

@app.route("/login")
def login():

    return render_template(
        "login.html"
    )

# =========================================
# REGISTRO
# =========================================

from database import db, Usuario, Historial


@app.route(
    "/registro"
)
def registro():

    return render_template(
        "registro.html"
    )


@app.route(
    "/api/registro",
    methods=["POST"]
)
def api_registro():

    try:

        data = request.get_json()

        nombre = data.get(
            "nombre"
        )

        email = data.get(
            "email"
        )

        password = data.get(
            "password"
        )

        existe = Usuario.query.filter_by(
            email=email
        ).first()

        if existe:

            return jsonify({

                "ok": False,

                "mensaje":
                "?? Correo ya registrado"

            })

        usuario = Usuario(

            nombre=nombre,

            email=email,

            password=password

        )

        db.session.add(
            usuario
        )

        db.session.commit()

        return jsonify({

            "ok": True,

            "mensaje":
            "? Cuenta creada"

        })

    except Exception as e:

        print(e)

        return jsonify({

            "ok": False,

            "mensaje":
            "? Error creando cuenta"

        })

# =========================================
# LOGIN API
# =========================================

from flask import session


@app.route(
    "/api/login",
    methods=["POST"]
)
def api_login():

    try:

        data = request.get_json()

        email = data.get(
            "usuario",
            ""
        )

        password = data.get(
            "password",
            ""
        )

        usuario = Usuario.query.filter_by(

            email=email,

            password=password

        ).first()

        if usuario:

            session["usuario"] = usuario.id

            return jsonify({

                "success": True,

                "nombre":
                usuario.nombre,

                "premium":
                usuario.premium

            })

        return jsonify({

            "success": False

        })

    except Exception as e:

        print(

            "ERROR LOGIN:",

            e

        )

        return jsonify({

            "success": False

        })

# =========================================
# HISTORIAL
# =========================================

@app.route(
"/historial"
)
def historial():

    usuario=session.get(
        "usuario"
    )

    if not usuario:

        return redirect(
            "/login"
        )

    datos=Historial.query.filter_by(

        usuario_id=usuario

    ).all()

    return render_template(

        "historial.html",

        historial=datos

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

        print(

            "ERROR CURSOS:",

            e

        )

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

        # GUARDAR HISTORIAL (sin romper el chat)
        try:

            usuario = session.get(
                "usuario"
            )

            if usuario:

                nuevo = Historial(

                    usuario_id=usuario,

                    pregunta=pregunta,

                    respuesta=respuesta

                )

                db.session.add(
                    nuevo
                )

                db.session.commit()

        except Exception as e:

            print(
                "ERROR HISTORIAL:",
                e
            )

        return jsonify({

            "respuesta":
            respuesta

        })

    except Exception as e:

        print(

            "ERROR CHAT:",

            e

        )

        return jsonify({

            "respuesta":

            "? Error"

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
		
		oa_codigo = oa.split(
            " - "
        )[0]

        oa_data = obtener_oa_completo(

            asignatura,
            curso,
            unidad,
            oa_codigo

        )
		
		indicadores = "\n".join([

            f"- {i}"

            for i in oa_data.get(
                "indicadores",
                []
            )

        ])

        habilidades = "\n".join([

            f"- {h}"

            for h in oa_data.get(
                "habilidades",
                []
            )

        ])

        evaluacion = "\n".join([

            f"- {e}"

            for e in oa_data.get(
                "evaluacion",
                []
            )

        ])

        actitudes = "\n".join([

            f"- {a}"

            for a in oa_data.get(
                "actitudes",
                []
            )

        ])		
		
       
        resultado = f"""

# PLANIFICACIÓN DOCENTE IA

---

## ASIGNATURA
{asignatura}

## CURSO
{curso}

## UNIDAD
{unidad}

---

## OBJETIVO DE APRENDIZAJE

{oa_data.get("descripcion", "")}

---

## INDICADORES

{indicadores}

---

## HABILIDADES

{habilidades}

---

## EVALUACIÓN

{evaluacion}

---

## ACTITUDES

{actitudes}

---

# EXPERIENCIA DE APRENDIZAJE

## INICIO

- Activación de conocimientos previos.
- Presentación del objetivo de la clase.
- Motivación inicial.
- Uso de material concreto.

---

## DESARROLLO

- Desarrollo guiado de actividades.
- Resolución de ejercicios.
- Trabajo colaborativo.
- Retroalimentación constante.
- Aplicación práctica del OA.

---

## CIERRE

- Síntesis de lo aprendido.
- Preguntas de metacognición.
- Ticket de salida.
- Retroalimentación grupal.

---

# ADECUACIONES NEE

- Apoyo visual.
- Uso de material concreto.
- Instrucciones segmentadas.
- Mediación docente.

---

# RECURSOS

- Pizarra
- Guía de trabajo
- Material concreto
- Tarjetas educativas

---

# TICKET DE SALIDA

- ¿Qué aprendiste hoy?
- Explica una actividad realizada.
- Representa un ejemplo relacionado con el OA.

"""
		
        # =====================================
        # OBJETIVOS
        # =====================================

        if data.get("objetivos"):

            resultado += """

#  Objetivos

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

#  Indicadores

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

#  Habilidades

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

#  Actitudes

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

#  Adaptaciones NEE

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

#  Evaluación

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

#  Error

No fue posible generar la planificación.

## Detalle técnico

{str(e)}

"""

        })


# =========================================
# MAIN
# =========================================

app.register_blueprint(auth)

# ====================================
# GENERAR IMAGEN
# ====================================

@app.route("/api/imagen", methods=["POST"])
def api_imagen():

    try:

        data = request.get_json()

        prompt = data.get(
            "prompt",
            ""
        )

        r = generar_imagen(
            prompt
        )

        return jsonify({

            "ok":
            r["ok"],

            "imagen":
            r.get(
                "imagen",
                ""
            ),

            "error":
            r.get(
                "error",
                ""
            )

        })

    except Exception as e:

        return jsonify({

            "ok": False,

            "error":
            str(e)

        })


