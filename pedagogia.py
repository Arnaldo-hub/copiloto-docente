# =========================================
# PEDAGOGIA.PY
# MOTOR IA PEDAGÓGICO PROFESIONAL
# =========================================

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
# GENERADOR IA CENTRAL
# =========================================

def generar_respuesta(prompt):

    try:

        response = client.chat.completions.create(

            model="gpt-4o-mini",

            messages=[

                {
                    "role": "system",
                    "content": """
Eres un experto pedagógico chileno especialista en:

- Currículum MINEDUC
- OA
- DUA
- NEE
- Evaluación auténtica
- Planificación
- Taxonomía de Bloom
- Aprendizaje basado en proyectos

Responde siempre en formato profesional docente.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.7

        )

        return (

            response
            .choices[0]
            .message
            .content

        )

    except Exception as e:

        print(
            "❌ Error OpenAI:",
            e
        )

        return """
Error generando contenido pedagógico.
Verifica OPENAI_API_KEY.
"""

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
Genera:

1. Objetivo general
2. 3 objetivos específicos

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

    return generar_respuesta(
        prompt
    )

# =========================================
# INDICADORES
# =========================================

def generar_indicadores(

    asignatura,
    curso,
    unidad,
    oa

):

    prompt = f"""
Genera 5 indicadores de evaluación.

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}

Formato:
• Indicador 1
• Indicador 2
"""

    return generar_respuesta(
        prompt
    )

# =========================================
# HABILIDADES
# =========================================

def generar_habilidades(

    asignatura,
    curso,
    unidad,
    oa

):

    prompt = f"""
Genera habilidades cognitivas,
procedimentales y actitudinales.

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}
"""

    return generar_respuesta(
        prompt
    )

# =========================================
# ACTITUDES
# =========================================

def generar_actitudes(

    asignatura,
    curso,
    unidad,
    oa

):

    prompt = f"""
Genera actitudes pedagógicas
alineadas al OA.

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}
"""

    return generar_respuesta(
        prompt
    )

# =========================================
# NEE
# =========================================

def generar_nee(

    asignatura,
    curso,
    unidad,
    oa

):

    prompt = f"""
Genera adaptaciones curriculares
y estrategias DUA para:

- TEA
- TDAH
- TEL
- Dislexia

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

    return generar_respuesta(
        prompt
    )

# =========================================
# EVALUACIÓN
# =========================================

def generar_evaluacion(

    asignatura,
    curso,
    unidad,
    oa

):

    prompt = f"""
Genera:

1. Evaluación diagnóstica
2. Evaluación formativa
3. Evaluación sumativa
4. Rúbrica breve

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}
"""

    return generar_respuesta(
        prompt
    )

# =========================================
# PLANIFICACIÓN IA
# =========================================

def generar_planificacion(

    asignatura,
    curso,
    unidad,
    oa

):

    prompt = f"""
Genera una planificación completa.

Debe incluir:

- Inicio
- Desarrollo
- Cierre
- Recursos
- Estrategias DUA
- Evaluación
- Tiempo estimado

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}

Formato profesional MINEDUC.
"""

    return generar_respuesta(
        prompt
    )
