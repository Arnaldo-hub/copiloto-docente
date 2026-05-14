import json
import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

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

def obtener_cursos(asignatura):

    data = leer_asignatura(asignatura)

    return list(data.keys())

def obtener_unidades(asignatura, curso):

    data = leer_asignatura(asignatura)

    if curso not in data:
        return []

    return data[curso]["unidades"]

def obtener_oa(asignatura, curso, unidad):

    data = leer_asignatura(asignatura)

    if curso not in data:
        return []

    unidades = data[curso]["unidades"]

    indice = int(unidad) - 1

    if indice < 0 or indice >= len(unidades):
        return []

    return unidades[indice]["oa"]
