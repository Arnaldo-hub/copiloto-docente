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

Responde SIEMPRE usando Markdown profesional.

Usa:

# Títulos
## Subtítulos
### Secciones

- bullets
- listas
- separación visual
- tablas cuando sea necesario

Formato visual moderno tipo:

- ChatGPT
- Notion
- Copilot
- MagicSchool AI

El contenido debe verse:
profesional,
ordenado,
limpio,
y fácil de leer para docentes.

"""
                },

                {
                    "role": "user",

                    "content": prompt
                }

            ],

           temperature=0.3,
max_tokens=700

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

# ❌ Error IA

No fue posible generar contenido pedagógico.

Verifica:

- OPENAI_API_KEY
- conexión OpenAI
- créditos API

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

# Generar Objetivos Pedagógicos

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

Usa formato profesional docente.

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

# Generar Indicadores

Genera 5 indicadores de evaluación.

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}

Incluye:

- habilidades
- desempeño esperado
- evidencia observable

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

# Generar Habilidades

Genera:

- habilidades cognitivas
- habilidades procedimentales
- habilidades actitudinales

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

# Generar Actitudes

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

# Adaptaciones NEE y DUA

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

Incluye:

- apoyos visuales
- adecuaciones
- participación
- accesibilidad

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

# Generar Evaluación

Genera:

## Evaluación diagnóstica
## Evaluación formativa
## Evaluación sumativa
## Rúbrica breve

Asignatura:
{asignatura}

Curso:
{curso}

Unidad:
{unidad}

OA:
{oa}

Incluye ejemplos concretos.

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

# Generar Planificación Completa

Genera una planificación profesional.

Debe incluir:

## Inicio
## Desarrollo
## Cierre
## Recursos
## Estrategias DUA
## Evaluación
## Tiempo estimado

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
