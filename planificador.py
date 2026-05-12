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
    oa

):

    prompt = f"""

Genera una planificación pedagógica chilena.

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}

Debe incluir:

- Objetivo
- Inicio
- Desarrollo
- Cierre
- Evaluación
- Adecuaciones NEE
- Recursos
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":"system",
                "content":"Eres experto curricular chileno."
            },

            {
                "role":"user",
                "content":prompt
            }

        ]

    )

    texto = (

        response
        .choices[0]
        .message
        .content

    )

    return texto
