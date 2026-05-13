import json
import os

DATA_PATH = "data"

def leer_asignatura(asignatura):
    archivo = asignatura.lower().replace(" ", "") + ".json"
    ruta = os.path.join(DATA_PATH, archivo)

    with open(ruta, encoding="utf-8") as f:
        return json.load(f)

def obtener_unidades(asignatura, curso):
    data = leer_asignatura(asignatura)
    return data.get(curso, {}).get("unidades", [])

def obtener_oa(asignatura, curso, unidad_nombre):
    data = leer_asignatura(asignatura)

    for unidad in data.get(curso, {}).get("unidades", []):
        if unidad["nombre"] == unidad_nombre:
            return unidad.get("oa", [])

    return []
