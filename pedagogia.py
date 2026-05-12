# =========================================
# PEDAGOGIA.PY
# MOTOR PEDAGÓGICO COPILOTO DOCENTE
# =========================================

from openai import OpenAI
import os

# =========================================
# OPENAI
# =========================================

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key
)

# =========================================
# OBJETIVOS
# =========================================

def generar_objetivos(
    asignatura,
    curso,
    unidad,
    oa
):

    prompt = f"""
Eres un experto pedagógico chileno.

Genera:

1. Objetivo general
2. Objetivo específico

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}

Formato profesional docente.
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":
                "system",

                "content":
                "Eres un experto pedagógico."
            },

            {
                "role":
                "user",

                "content":
                prompt
            }

        ]

    )

    return (
        response
        .choices[0]
        .message
        .content
    )

# =========================================
# INDICADORES
# =========================================

def generar_indicadores(
    asignatura,
    curso,
    oa
):

    prompt = f"""
Genera indicadores de evaluación
para el siguiente OA.

Asignatura:
{asignatura}

Curso:
{curso}

OA:
{oa}

Formato:
- indicador 1
- indicador 2
- indicador 3
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":
                "user",

                "content":
                prompt
            }

        ]

    )

    return (
        response
        .choices[0]
        .message
        .content
    )

# =========================================
# HABILIDADES
# =========================================

def generar_habilidades(
    asignatura,
    curso,
    oa
):

    prompt = f"""
Genera habilidades pedagógicas
relacionadas al OA.

Asignatura:
{asignatura}

Curso:
{curso}

OA:
{oa}
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":
                "user",

                "content":
                prompt
            }

        ]

    )

    return (
        response
        .choices[0]
        .message
        .content
    )

# =========================================
# ACTITUDES
# =========================================

def generar_actitudes(
    asignatura,
    curso
):

    prompt = f"""
Genera actitudes pedagógicas
para:

Asignatura:
{asignatura}

Curso:
{curso}
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":
                "user",

                "content":
                prompt
            }

        ]

    )

    return (
        response
        .choices[0]
        .message
        .content
    )

# =========================================
# NEE
# =========================================

def generar_nee(
    asignatura,
    curso,
    oa
):

    prompt = f"""
Genera adaptaciones NEE para:

- TEA
- TDAH
- TEL
- Dislexia

Asignatura:
{asignatura}

Curso:
{curso}

OA:
{oa}
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":
                "user",

                "content":
                prompt
            }

        ]

    )

    return (
        response
        .choices[0]
        .message
        .content
    )

# =========================================
# EVALUACIONES
# =========================================

def generar_evaluacion(
    asignatura,
    curso,
    oa
):

    prompt = f"""
Genera:

1. Evaluación diagnóstica
2. Evaluación formativa
3. Evaluación sumativa

Asignatura:
{asignatura}

Curso:
{curso}

OA:
{oa}
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[

            {
                "role":
                "user",

                "content":
                prompt
            }

        ]

    )

    return (
        response
        .choices[0]
        .message
        .content
    )
