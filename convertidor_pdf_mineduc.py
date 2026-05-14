import fitz
import re
import json
import os

# =========================================
# PDF OFICIAL
# =========================================

PDF = "pdfs/Bases Curriculares 1° a 6° Básico.pdf"

# =========================================
# EXTRAER TEXTO
# =========================================

doc = fitz.open(PDF)

texto = ""

for pagina in doc:

    texto += pagina.get_text()

# =========================================
# EXTRAER SECCIÓN LENGUAJE
# =========================================

inicio = texto.find(
    "Lenguaje y Comunicación"
)

fin = texto.find(
    "Matemática"
)

contenido = texto[inicio:fin]

# =========================================
# EXTRAER OA
# =========================================

patron = r"OA\s+\d+"

coincidencias = list(
    re.finditer(
        patron,
        contenido
    )
)

oa = []

for i in range(len(coincidencias)):

    inicio_oa = coincidencias[i].start()

    if i + 1 < len(coincidencias):

        fin_oa = coincidencias[i + 1].start()

    else:

        fin_oa = len(contenido)

    bloque = contenido[
        inicio_oa:fin_oa
    ]

    codigo_match = re.search(
        r"OA\s+\d+",
        bloque
    )

    if codigo_match:

        codigo = codigo_match.group()

        descripcion = bloque.replace(
            codigo,
            ""
        )

        descripcion = " ".join(
            descripcion.split()
        )

        descripcion = descripcion[:400]

        oa.append({

            "codigo": codigo,
            "descripcion": descripcion

        })

# =========================================
# GENERAR UNIDADES
# =========================================

unidades = []

grupo = []

numero = 1

for item in oa:

    grupo.append(item)

    if len(grupo) == 5:

        unidades.append({

            "numero": numero,

            "nombre":
            f"Unidad {numero}",

            "semestre":
            1 if numero <= 2 else 2,

            "proposito":
            "Unidad generada desde Bases Curriculares oficiales MINEDUC.",

            "oa":
            grupo

        })

        grupo = []

        numero += 1

# =========================================
# JSON FINAL
# =========================================

estructura = {

    "1° Básico": {

        "nombre_asignatura":
        "Lenguaje y Comunicación",

        "programa":
        "MINEDUC",

        "unidades":
        unidades

    }

}

os.makedirs("data", exist_ok=True)

with open(

    "data/lenguaje.json",
    "w",
    encoding="utf-8"

) as archivo:

    json.dump(

        estructura,
        archivo,
        ensure_ascii=False,
        indent=2

    )

print("✅ lenguaje.json generado correctamente")
