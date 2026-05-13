from openai import OpenAI
import os

api_key = os.getenv(
    "OPENAI_API_KEY"
)

client = OpenAI(
    api_key=api_key
)

def generar_planificacion(

    asignatura,
    curso,
    unidad,
    oa,
    opciones

):

    secciones = []

    if opciones.get("objetivos"):
        secciones.append("Objetivos")

    if opciones.get("indicadores"):
        secciones.append("Indicadores")

    if opciones.get("habilidades"):
        secciones.append("Habilidades")

    if opciones.get("actitudes"):
        secciones.append("Actitudes")

    if opciones.get("evaluacion"):
        secciones.append("Evaluación")

    if opciones.get("nee"):
        secciones.append("Adecuaciones NEE")

    if opciones.get("recursos"):
        secciones.append("Recursos")

    estructura = "\\n".join(secciones)

    prompt = f"""

Genera una planificación pedagógica chilena profesional.

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}

Debe incluir SOLO:

{estructura}

"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":"system",
                "content":"Eres un experto curricular chileno."
            },

            {
                "role":"user",
                "content":prompt
            }

        ]

    )

    return (

        response
        .choices[0]
        .message
        .content

    )
