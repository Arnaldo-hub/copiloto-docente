import json
import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

# =========================================
# LEER JSON
# =========================================

def leer_asignatura(asignatura):

    ruta = os.path.join(
        DATA_DIR,
        f"{asignatura}.json"
    )

    with open(
        ruta,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)

# =========================================
# OBTENER CURSOS
# =========================================

def obtener_cursos(asignatura):

    data = leer_asignatura(asignatura)

    return list(data.keys())

# =========================================
# OBTENER UNIDADES
# =========================================

def obtener_unidades(asignatura, curso):

    data = leer_asignatura(asignatura)

    if curso not in data:

        return []

    unidades = data[curso].get(
        "unidades",
        []
    )

    resultado = []

    for unidad in unidades:

        if isinstance(unidad, dict):

            resultado.append({

                "nombre":
                unidad.get(
                    "nombre",
                    "Unidad"
                )

            })

        else:

            resultado.append({

                "nombre":
                str(unidad)

            })

    return resultado

# =========================================
# OBTENER OA
# =========================================

def obtener_oa(

    asignatura,
    curso,
    unidad_nombre

):

    data = leer_asignatura(asignatura)

    if curso not in data:

        return []

    unidades = data[curso].get(
        "unidades",
        []
    )

    for unidad in unidades:

        if isinstance(unidad, dict):

            if unidad.get(
                "nombre"
            ) == unidad_nombre:

                return unidad.get(
                    "oa",
                    []
                )

    return []