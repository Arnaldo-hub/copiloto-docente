import os
import re
import json
import fitz
# =========================================
# CONFIGURACIÓN
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PDF_DIR = os.path.join(
    BASE_DIR,
    "pdfs"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(DATA_DIR, exist_ok=True)
# =========================================
# MAPEO ASIGNATURAS
# =========================================

ASIGNATURAS = {

    "leng": "lenguaje",
    "mat": "matematica",
    "HIST": "historia",
    "EFI": "educacionfisica",
    "Música": "musica",
    "tecnol": "tecnologia",
    "Orientación": "orientacion",
    "artes": "artesvisuales"

}
# =========================================
# EXTRAER TEXTO PDF
# =========================================


def extraer_texto_pdf(ruta_pdf):

    texto = ""

    documento = fitz.open(ruta_pdf)

    for pagina in documento:

        texto += pagina.get_text()

    return texto
    # =========================================

    patron = r"OA\s+\d+"

    coincidencias = list(
        re.finditer(patron, texto)
    )

    oa = []

    for i in range(len(coincidencias)):

        inicio = coincidencias[i].start()

        if i + 1 < len(coincidencias):

            fin = coincidencias[i + 1].start()

        else:

            fin = len(texto)

        bloque = texto[inicio:fin]

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

            descripcion = descripcion[:500]

            oa.append({

                "codigo": codigo,
                "descripcion": descripcion

            })

    return oa
    # =========================================

            unidades.append({

                "numero": numero,

                "nombre": f"Unidad {numero}",

                "semestre": 1 if numero <= 2 else 2,

                "proposito": "Unidad curricular construida automáticamente desde Programa de Estudio MINEDUC.",

                "oa": unidad_actual

            })

            unidad_actual = []

            numero += 1

    if unidad_actual:

        unidades.append({

            "numero": numero,

            "nombre": f"Unidad {numero}",

            "semestre": 2,

            "proposito": "Unidad curricular construida automáticamente desde Programa de Estudio MINEDUC.",

            "oa": unidad_actual

        })

    return unidades
# =========================================

        curso: {

            "nombre_asignatura": nombre_json,

            "programa": "MINEDUC",

            "unidades": generar_unidades(oa)

        }

    }

    ruta_salida = os.path.join(

        DATA_DIR,
        f"{nombre_json}.json"

    )

    with open(

        ruta_salida,
        "w",
        encoding="utf-8"

    ) as archivo:

        json.dump(

            estructura,
            archivo,
            ensure_ascii=False,
            indent=2

        )

    print(f"✅ Generado: {ruta_salida}")
# =========================================
# MAIN
# =========================================


def main():

    archivos = os.listdir(PDF_DIR)

    for archivo in archivos:

        if not archivo.endswith(".pdf"):
            continue

        ruta = os.path.join(
            PDF_DIR,
            archivo
        )

        texto = extraer_texto_pdf(ruta)

        oa = extraer_oa(texto)

        nombre_json = None

        for clave, valor in ASIGNATURAS.items():

            if clave.lower() in archivo.lower():

                nombre_json = valor
                break

        if not nombre_json:
            continue

        generar_json(
            nombre_json,
            "1° Básico",
            oa
        )


if __name__ == "__main__":

    main()
