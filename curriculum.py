# =========================================
# CURRICULUM.PY
# MOTOR CURRICULAR CHILENO
# =========================================

import json
import os

# =========================================
# RUTA DATA
# =========================================

DATA_PATH = "data"

# =========================================
# LEER JSON
# =========================================

def leer_asignatura(asignatura):

    archivo = (
        asignatura
        .lower()
        .replace(" ", "")
        + ".json"
    )

    ruta = os.path.join(

        DATA_PATH,
        archivo

    )

    with open(

        ruta,
        encoding="utf-8"

    ) as f:

        return json.load(f)

# =========================================
# CURSOS
# =========================================

def obtener_cursos(asignatura):

    data = leer_asignatura(asignatura)

    return list(data.keys())

# =========================================
# UNIDADES
# =========================================

def obtener_unidades(

    asignatura,
    curso

):

    data = leer_asignatura(asignatura)

    curso_data = data.get(curso)

    if not curso_data:

        return []

    return curso_data.get(

        "unidades",
        []

    )

# =========================================
# OA
# =========================================

def obtener_oa(

    asignatura,
    curso,
    unidad_nombre

):

    data = leer_asignatura(asignatura)

    curso_data = data.get(curso)

    if not curso_data:

        return []

    unidades = curso_data.get(

        "unidades",
        []

    )

    for unidad in unidades:

        if unidad["nombre"] == unidad_nombre:

            return unidad.get(

                "oa",
                []

            )

    return []
