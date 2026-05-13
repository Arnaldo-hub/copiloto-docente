
import json
import os

DATA_PATH = "data"

def leer_asignatura(asignatura):

    ruta = os.path.join(DATA_PATH, f"{asignatura}.json")

    with open(ruta, encoding="utf-8") as f:
        return json.load(f)

def obtener_cursos(asignatura):

    data = leer_asignatura(asignatura)

    return list(data.keys())

def obtener_unidades(asignatura, curso):

    data = leer_asignatura(asignatura)

    return data[curso]["unidades"]

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

    unidades = data[curso]["unidades"]

    indice = int(unidad) - 1

    if indice >= 0 and indice < len(unidades):

        return unidades[indice]["oa"]

    return []

    data = leer_asignatura(asignatura)

    unidades = data[curso]["unidades"]

    for unidad in unidades:

        if unidad["nombre"] == unidad_nombre:
            return unidad["oa"]

    return []
