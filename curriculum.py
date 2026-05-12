
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

def obtener_oa(asignatura, curso, unidad_nombre):

    data = leer_asignatura(asignatura)

    unidades = data[curso]["unidades"]

    for unidad in unidades:

        if unidad["nombre"] == unidad_nombre:
            return unidad["oa"]

    return []
