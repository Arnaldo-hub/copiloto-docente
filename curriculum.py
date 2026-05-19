import json
import os
from functools import lru_cache

# =========================================
# RUTAS
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

# =========================================
# VALIDAR ARCHIVO
# =========================================

def existe_json(asignatura):

    ruta = os.path.join(
        DATA_DIR,
        f"{asignatura}.json"
    )

    return os.path.exists(ruta)

# =========================================
# LEER JSON
# =========================================

@lru_cache(maxsize=50)
def leer_asignatura(asignatura):

    if not existe_json(asignatura):

        return {}

    ruta = os.path.join(
        DATA_DIR,
        f"{asignatura}.json"
    )

    try:

        with open(
            ruta,
            "r",
            encoding="utf-8"
        ) as archivo:

            return json.load(archivo)

    except Exception as e:

        print(
            f"❌ Error leyendo {asignatura}.json:",
            e
        )

        return {}

# =========================================
# OBTENER CURSOS
# =========================================

def obtener_cursos(asignatura):

    data = leer_asignatura(
        asignatura
    )

    return list(data.keys())

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

    return data[curso].get(
        "unidades",
        []
    )

# =========================================
# OBTENER OA
# =========================================

def obtener_oa(

    asignatura,
    curso,
    unidad_nombre

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

    for unidad in unidades:

        if unidad.get(
            "nombre"
        ) == unidad_nombre:

            return unidad.get(
                "oa",
                []
            )

    return []

# =========================================
# BUSCADOR IA
# =========================================

def buscar_oa_global(texto):

    resultados = []

    archivos = os.listdir(
        DATA_DIR
    )

    for archivo in archivos:

        if not archivo.endswith(".json"):

            continue

        asignatura = archivo.replace(
            ".json",
            ""
        )

        data = leer_asignatura(
            asignatura
        )

        for curso, contenido in data.items():

            unidades = contenido.get(
                "unidades",
                []
            )

            for unidad in unidades:

                oa_lista = unidad.get(
                    "oa",
                    []
                )

                for oa in oa_lista:

                    if texto.lower() in oa.lower():

                        resultados.append({

                            "asignatura": asignatura,
                            "curso": curso,
                            "unidad": unidad.get(
                                "nombre"
                            ),
                            "oa": oa

                        })

    return resultados
