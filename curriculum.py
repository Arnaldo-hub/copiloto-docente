import json
import os

# =========================================
# RUTA DATA
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

# =========================================
# LEER ASIGNATURA
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

        data = json.load(
            archivo
        )

    return data

# =========================================
# OBTENER ASIGNATURAS
# =========================================

def obtener_asignaturas():

    asignaturas = []

    for archivo in os.listdir(DATA_DIR):

        if archivo.endswith(".json"):

            nombre = archivo.replace(
                ".json",
                ""
            )

            asignaturas.append(
                nombre
            )

    asignaturas.sort()

    return asignaturas

# =========================================
# OBTENER CURSOS
# =========================================

def obtener_cursos(asignatura):

    data = leer_asignatura(
        asignatura
    )

    cursos = list(
        data.keys()
    )

    return cursos

# =========================================
# OBTENER UNIDADES
# =========================================

def obtener_unidades(

    asignatura,
    curso

):

    data = leer_asignatura(
        asignatura
    )

    if curso not in data:

        return []

    unidades = data[curso].get(
        "unidades",
        []
    )

    resultado = []

    for unidad in unidades:

        resultado.append({

            "nombre":
            unidad.get(
                "nombre",
                "Unidad sin nombre"
            )

        })

    return resultado

# =========================================
# OBTENER OA
# =========================================

def obtener_oa(

    asignatura,
    curso,
    unidad

):

    data = leer_asignatura(
        asignatura
    )

    if curso not in data:

        return []

    unidades = data[curso].get(
        "unidades",
        []
    )

    indice = int(unidad) - 1

    if indice < 0:

        return []

    if indice >= len(unidades):

        return []

    oa = unidades[indice].get(
        "oa",
        []
    )

    resultado = []

    for objetivo in oa:

        resultado.append({

            "codigo":
            objetivo.get(
                "codigo",
                "OA"
            ),

            "descripcion":
            objetivo.get(
                "descripcion",
                ""
            )

        })

    return resultado
