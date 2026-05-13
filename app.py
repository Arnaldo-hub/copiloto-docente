# Sistema de Login con usuarios.json para Copiloto Docente IA

## Estructura esperada

```text
usuarios/
├── usuarios.json
```

---

# 1. Crear carpeta

Crear:

```text
usuarios
```

En la raíz del proyecto.

---

# 2. Crear archivo

```text
usuarios/usuarios.json
```

Contenido:

```json
[
    {
        "usuario": "admin",
        "password": "1234",
        "nombre": "Administrador"
    },
    {
        "usuario": "docente1",
        "password": "abcd",
        "nombre": "Docente 1"
    }
]
```

---

# 3. Reemplazar COMPLETO app.py

```python
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
# LOGIN
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

    usuario = data.get("usuario")
    password = data.get("password")

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
                "success": True
            })

    return jsonify({
        "success": False
    })


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

@app.route("/api/cursos/<asignatura>")
def api_cursos(asignatura):

    return jsonify({
        "cursos":obtener_cursos(asignatura)
    })

# =========================================
# UNIDADES
# =========================================

@app.route(
    "/api/unidades/<asignatura>/<curso>"
)
def api_unidades(asignatura, curso):

    return jsonify({
        "unidades":obtener_unidades(
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
def api_oa(asignatura, curso, unidad):

    return jsonify({
        "oa":obtener_oa(
            asignatura,
            curso,
            unidad
        )
    })

# =========================================
# PLANIFICADOR
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
            "resultado":resultado
        })

    except Exception as e:

        return jsonify({
            "resultado":str(e)
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
```

---

# 4. Crear templates/login.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Login</title>

<style>

body{
background:#03133b;
font-family:Arial;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
margin:0;
}

.card{
background:#182952;
padding:40px;
border-radius:20px;
width:360px;
}

h1{
color:white;
margin-bottom:25px;
text-align:center;
}

input{
width:100%;
padding:15px;
border:none;
border-radius:12px;
margin-bottom:18px;
font-size:18px;
}

button{
width:100%;
padding:16px;
border:none;
border-radius:12px;
background:#22c55e;
color:white;
font-size:20px;
font-weight:bold;
cursor:pointer;
}

#error{
color:#ff7b7b;
margin-top:15px;
text-align:center;
}

</style>

</head>
<body>

<div class="card">

<h1>
🔐 Login Docente
</h1>

<input
id="usuario"
placeholder="Usuario">

<input
id="password"
type="password"
placeholder="Contraseña">

<button onclick="login()">
Ingresar
</button>

<div id="error"></div>

</div>

<script>

async function login(){

const usuario =
document.getElementById(
'usuario'
).value

const password =
document.getElementById(
'password'
).value

const res = await fetch(
'/api/login',
{
method:'POST',
headers:{
'Content-Type':'application/json'
},
body:JSON.stringify({
usuario,
password
})
}
)

const data = await res.json()

if(data.success){
window.location='/'
}else{
document.getElementById(
'error'
).innerHTML =
'Usuario o contraseña incorrectos'
}

}

</script>

</body>
</html>
```

---

# Resultado final

Tendrás:

* Login funcional
* usuarios.json
* sesión persistente
* protección de la plataforma
* logout
* acceso profesional tipo SaaS educativo
* base lista para:

  * planes premium
  * historial por usuario
  * estadísticas
  * roles docentes
