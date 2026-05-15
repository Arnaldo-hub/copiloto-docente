import re
import json
import os

# =========================================
# CARPETAS
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
# LIMPIEZA CURRICULAR
# =========================================

def limpiar_texto(texto):

    basura = [

        "Ministerio de Educación",
        "Programa de Estudio",
        "Unidad de Currículum y Evaluación",
        "www.curriculumnacional.cl",
        "curriculumnacional.cl",
        "Gobierno de Chile",
        "Mineduc",
        "Bases Curriculares",
        "Educación Básica"

    ]

    for item in basura:

        texto = texto.replace(
            item,
            ""
        )

    # eliminar saltos múltiples
    texto = re.sub(
        r"\n+",
        "\n",
        texto
    )

    # eliminar espacios múltiples
    texto = re.sub(
        r"[ \t]+",
        " ",
        texto
    )

    return texto.strip()

# =========================================
# EXTRAER OA REALES
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

        if not codigo_match:
            continue

        codigo = codigo_match.group()

        descripcion = bloque.replace(
            codigo,
            ""
        )

        descripcion = descripcion.strip()

        # limpiar exceso texto
        descripcion = re.sub(
            r"\s+",
            " ",
            descripcion
        )

        # cortar basura extrema
        descripcion = descripcion[:700]

        # ignorar descripciones vacías
        if len(descripcion) < 15:
            continue

        oa.append({

            "codigo": codigo,
            "descripcion": descripcion

        })

    return oa

# =========================================
# DETECTAR UNIDADES REALES
# =========================================

def detectar_unidades(texto):

    patrones = [

        r"Unidad\s+\d+",
        r"UNIDAD\s+\d+"

    ]

    unidades = []

    numero = 1

    for patron in patrones:

        coincidencias = re.findall(
            patron,
            texto
        )

        for item in coincidencias:

            unidades.append({

                "numero": numero,
                "nombre": item

            })

            numero += 1

    # evitar duplicados
    nombres = set()

    unidades_limpias = []

    for unidad in unidades:

        if unidad["nombre"] not in nombres:

            nombres.add(
                unidad["nombre"]
            )

            unidades_limpias.append(
                unidad
            )

    return unidades_limpias

# =========================================
# DETECTAR TÍTULOS PEDAGÓGICOS
# =========================================

def detectar_titulos(texto):

    patron = r"[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ]{5,}"

    coincidencias = re.findall(
        patron,
        texto
    )

    titulos = []

    for item in coincidencias:

        item = item.strip()

        if len(item) > 80:
            continue

        titulos.append(item)

    return list(set(titulos))

# =========================================
# AGRUPAR OA POR UNIDAD
# =========================================

def agrupar_oa_unidades(

    oa,
    unidades

):

    estructura = []

    indice = 0

    for unidad in unidades:

        grupo = oa[indice:indice+5]

        estructura.append({

            "numero":
            unidad["numero"],

            "nombre":
            unidad["nombre"],

            "semestre":
            1 if unidad["numero"] <= 2 else 2,

            "proposito":
            "Unidad curricular detectada automáticamente desde documentos oficiales MINEDUC.",

            "oa":
            grupo

        })

        indice += 5

    return estructura

# =========================================
# GENERAR JSON
# =========================================

def generar_json(

    nombre,
    unidades_finales,
    titulos

):

    estructura = {

        "1° Básico": {

            "nombre_asignatura":
            nombre,

            "programa":
            "MINEDUC",

            "titulos_detectados":
            titulos,

            "unidades":
            unidades_finales

        }

    }

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

    print(
        f"✅ JSON generado: {ruta}"
    )

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

        titulos = detectar_titulos(texto)

        unidades_finales = agrupar_oa_unidades(

            oa,
            unidades

        )

        nombre = archivo.replace(
            ".txt",
            ""
        ).lower()

        generar_json(

            nombre,
            unidades_finales,
            titulos

        )

# =========================================
# EJECUCIÓN
# =========================================

if __name__ == "__main__":

    main()
