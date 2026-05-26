import json
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


# =====================================
# LEER JSON
# =====================================

def leer_asignatura(asignatura):

    ruta = os.path.join(
        DATA_DIR,
        f"{asignatura}.json"
    )

    if not os.path.exists(ruta):

        return {}

    with open(
        ruta,
        "r",
        encoding="utf-8"
    ) as archivo:

        data = json.load(
            archivo
        )

    if asignatura in data:

        return data[asignatura]

    return data


# =====================================
# CURSOS
# =====================================

def obtener_cursos(
    asignatura
):

    data = leer_asignatura(
        asignatura
    )

    return list(
        data.keys()
    )


# =====================================
# UNIDADES
# =====================================

def obtener_unidades(

    asignatura,
    curso

):

    data = leer_asignatura(
        asignatura
    )

    if curso not in data:

        return []

    resultado = []

    for unidad in data[curso]:

        resultado.append({

            "nombre":
            unidad

        })

    return resultado


# =====================================
# OA
# =====================================

def obtener_oa(

    asignatura,
    curso,
    unidad

):

    data = leer_asignatura(
        asignatura
    )

    try:

        return list(

            data[
                curso
            ][
                unidad
            ].keys()

        )

    except:

        return []


# =====================================
# DETALLE OA
# =====================================

def obtener_detalle_oa(

    asignatura,
    curso,
    unidad,
    oa

):

    data = leer_asignatura(
        asignatura
    )

    try:

        return (

            data[
                curso
            ][
                unidad
            ][
                oa
            ]

        )

    except:

        return {}
