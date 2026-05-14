import json
import re

PDF_TXT = "lenguaje_mineduc.txt"

SALIDA_JSON = "data/lenguaje.json"

# ==========================================
# EXTRAER OA
# ==========================================

def extraer_oa(texto):

    patron = r"OA\s+\d+.*?(?=OA\s+\d+|$)"

    encontrados = re.findall(
        patron,
        texto,
        re.DOTALL
    )

    oa_limpios = []

    for item in encontrados:

        lineas = item.split("\n")

        contenido = " ".join(
            l.strip()
            for l in lineas
            if l.strip()
        )

        codigo = re.search(
            r"(OA\s+\d+)",
            contenido
        )

        if codigo:

            codigo_oa = codigo.group(1)

            descripcion = contenido.replace(
                codigo_oa,
                ""
            ).strip()

            oa_limpios.append({

                "codigo": codigo_oa,
                "descripcion": descripcion

            })

    return oa_limpios

# ==========================================
# GENERAR UNIDADES
# ==========================================

def generar_unidades(oa):

    unidades = []

    unidad_actual = []

    numero = 1

    for item in oa:

        unidad_actual.append(item)

        if len(unidad_actual) == 3:

            unidades.append({

                "numero": numero,

                "nombre": f"Unidad {numero}",

                "semestre": 1 if numero <= 2 else 2,

                "proposito": "Unidad construida desde OA oficiales MINEDUC.",

                "oa": unidad_actual,

                "habilidades": [

                    "Comprensión",
                    "Comunicación",
                    "Pensamiento crítico"

                ],

                "actitudes": [

                    "Participación",
                    "Respeto",
                    "Autonomía"

                ],

                "evaluaciones": [

                    "Rúbrica",
                    "Lista de cotejo",
                    "Evaluación formativa"

                ],

                "nee": [

                    "Apoyo visual",
                    "Adecuación curricular",
                    "Andamiaje"

                ]

            })

            unidad_actual = []

            numero += 1

    return unidades

# ==========================================
# MAIN
# ==========================================

with open(

    PDF_TXT,
    "r",
    encoding="utf-8"

) as archivo:

    texto = archivo.read()

oa = extraer_oa(texto)

estructura = {

    "1° Básico": {

        "nombre_asignatura":
        "Lenguaje y Comunicación",

        "ejes": [

            "Lectura",
            "Escritura",
            "Comunicación Oral"

        ],

        "unidades":
        generar_unidades(oa)

    }

}

with open(

    SALIDA_JSON,
    "w",
    encoding="utf-8"

) as salida:

    json.dump(

        estructura,
        salida,
        ensure_ascii=False,
        indent=2

    )

print("✅ lenguaje.json generado correctamente")
