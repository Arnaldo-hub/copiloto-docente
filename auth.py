from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    render_template,
    redirect
)

# =========================================
# BLUEPRINT
# =========================================

auth = Blueprint(

    "auth",

    __name__

)

# =========================================
# USUARIOS TEMPORALES
# (después pasaremos a BD)
# =========================================

USUARIOS = {

    "admin": {

        "password": "1234",

        "nombre":
        "Administrador"

    },

    "docente": {

        "password": "docente",

        "nombre":
        "Docente"

    }

}

# =========================================
# LOGIN
# =========================================

@auth.route(
    "/login"
)
def login():

    if session.get(
        "usuario"
    ):

        return redirect("/")

    return render_template(

        "login.html"

    )

# =========================================
# API LOGIN
# =========================================

@auth.route(
    "/api/login",
    methods=["POST"]
)
def api_login():

    try:

        data = request.json

        usuario = data.get(
            "usuario",
            ""
        )

        password = data.get(
            "password",
            ""
        )

        if (

            usuario in USUARIOS

            and

            USUARIOS[
                usuario
            ]["password"]

            ==

            password

        ):

            session[
                "usuario"
            ] = {

                "usuario":
                usuario,

                "nombre":
                USUARIOS[
                    usuario
                ][
                    "nombre"
                ]

            }

            return jsonify({

                "success": True

            })

        return jsonify({

            "success": False

        })

    except Exception as e:

        print(
            "LOGIN ERROR:",
            e
        )

        return jsonify({

            "success": False

        })

# =========================================
# PERFIL
# =========================================

@auth.route(
    "/api/me"
)
def me():

    usuario = session.get(
        "usuario"
    )

    if not usuario:

        return jsonify({

            "auth": False

        })

    return jsonify({

        "auth": True,

        "usuario":
        usuario

    })

# =========================================
# LOGOUT
# =========================================

@auth.route(
    "/logout"
)
def logout():

    session.clear()

    return redirect(
        "/login"
    )
