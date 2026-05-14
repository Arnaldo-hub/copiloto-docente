import fitz
import json
import re

PDF = "Bases Curriculares 1° a 6° Básico(1).pdf"

SALIDA = "data/lenguaje.json"

# =========================================
# EXTRAER TEXTO PDF
# =========================================

doc = fitz.open(PDF)

texto = ""

for pagina in doc:

    texto += pagina.get_text()

# =========================================
# BUSCAR OA LENGUAJE
# =========================================

inicio = texto.find("Lenguaje y Comunicación")

fin = texto.find("Música")

contenido = texto[inicio:fin]

patron = r"OA\s+\d+"

matches = list(re.finditer(patron, contenido))

oa = []

for i in range(len(matches)):

    inicio_oa = matches[i].start()

    if i + 1 < len(matches):

        fin_oa = matches[i + 1].start()

    else:

        fin_oa = len(contenido)

    bloque = contenido[inicio_oa:fin_oa]

    codigo = re.search(r"OA\s+\d+", bloque)

    if codigo:

        codigo_texto = codigo.group()

        descripcion = bloque.replace(
            codigo_texto,
            ""
        ).strip()

        descripcion = " ".join(
            descripcion.split()
        )

        oa.append({

            "codigo": codigo_texto,

            "descripcion": descripcion

        })

# =========================================
# GENERAR JSON
# =========================================

estructura = {

    "1° Básico": {

        "nombre_asignatura":
        "Lenguaje y Comunicación",

        "ejes": [

            "Lectura",
            "Escritura",
            "Comunicación Oral"

        ],

        "unidades": [

            {

                "numero": 1,

                "nombre":
                "Unidad generada automáticamente",

                "semestre": 1,

                "proposito":
                "Unidad construida desde Bases Curriculares oficiales.",

                "oa": oa[:10]

            }

        ]

    }

}

with open(

    SALIDA,
    "w",
    encoding="utf-8"

) as archivo:

    json.dump(

        estructura,
        archivo,
        ensure_ascii=False,
        indent=2

    )

print("✅ lenguaje.json generado desde PDF oficial")
