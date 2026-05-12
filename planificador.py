from openai import OpenAI
import os

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
# GENERAR PLANIFICACIÓN
# =========================================

def generar_planificacion(

    asignatura,
    curso,
    unidad,
    oa

):

    prompt = f"""

Eres un experto pedagógico chileno.

Genera una planificación docente completa.

ASIGNATURA:
{asignatura}

CURSO:
{curso}

UNIDAD:
{unidad}

OA:
{oa}

La planificación debe incluir:

1. Objetivo de la clase

2. Inicio
- motivación
- activación de conocimientos previos

3. Desarrollo
- actividades principales
- trabajo guiado
- estrategias pedagógicas

4. Cierre
- reflexión
- metacognición

5. Evaluación
- evaluación formativa
- ticket de salida

6. Adecuaciones NEE

7. Recursos

8. Tiempo estimado

Formato profesional.
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":"system",

                "content":
                "Eres un experto curricular chileno."
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
