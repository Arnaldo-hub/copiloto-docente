import re
import json
import os

# =========================================
# CONFIGURACIÓN
# =========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TXT_DIR = os.path.join(
    BASE_DIR,
    "txt"
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

os.makedirs(DATA_DIR, exist_ok=True)

# =========================================
# LIMPIAR TEXTO
# =========================================

def limpiar_texto(texto):

    # eliminar saltos múltiples
    texto = re.sub(
        r"\n+",
        "\n",
        texto
    )

    # eliminar espacios múltiples
    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    # eliminar páginas típicas
    texto = re.sub(
        r"Ministerio de Educación.*?",
        "",
        texto
    )

    texto = re.sub(
        r"Unidad de Currículum y Evaluación.*?",
        "",
        texto
    )

    return texto.strip()

# =========================================
# EXTRAER OA
# =========================================

def extraer_oa(texto):

    patron = r"(OA\s+\d+)"

    coincidencias = list(
        re.finditer(
            patron,
            texto
        )
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
            patron,
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
# DETECTAR UNIDADES
# =========================================

def detectar_unidades(texto):

    patron = r"(Unidad\s+\d+)"

    coincidencias = re.findall(
        patron,
        texto
    )

    unidades = []

    numero = 1

    for item in coincidencias:

        unidades.append({

            "numero": numero,
            "nombre": item

        })

        numero += 1

    return unidades

# =========================================
# GENERAR JSON
# =========================================

def generar_json(nombre, oa, unidades):

    estructura = {

        "1° Básico": {

            "nombre_asignatura":
            nombre,

            "programa":
            "MINEDUC",

            "unidades": []

        }

    }

    indice = 0

    for unidad in unidades:

        grupo = oa[indice:indice+5]

        estructura["1° Básico"]["unidades"].append({

            "numero":
            unidad["numero"],

            "nombre":
            unidad["nombre"],

            "semestre":
            1 if unidad["numero"] <= 2 else 2,

            "proposito":
            "Unidad generada automáticamente desde Programa MINEDUC.",

            "oa":
            grupo

        })

        indice += 5

    ruta = os.path.join(

        DATA_DIR,
        f"{nombre}.json"

    )

    with open(

        ruta,
        "w",
        encoding="utf-8"

    ) as archivo:

        json.dump(

            estructura,
            archivo,
            ensure_ascii=False,
            indent=2

        )

    print(f"✅ JSON generado: {ruta}")

# =========================================
# MAIN
# =========================================

def main():

    archivos = os.listdir(TXT_DIR)

    for archivo in archivos:

        if not archivo.endswith(".txt"):
            continue

        ruta = os.path.join(
            TXT_DIR,
            archivo
        )

        with open(

            ruta,
            "r",
            encoding="utf-8"

        ) as f:

            texto = f.read()

        texto = limpiar_texto(texto)

        oa = extraer_oa(texto)

        unidades = detectar_unidades(texto)

        nombre = archivo.replace(
            ".txt",
            ""
        )

        generar_json(

            nombre,
            oa,
            unidades

        )

# =========================================
# EJECUCIÓN
# =========================================

if __name__ == "__main__":

    main()
