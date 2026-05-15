import fitz
import os

# =========================================
# CARPETAS
# =========================================

PDF_DIR = "pdfs"
TXT_DIR = "txt"

os.makedirs(TXT_DIR, exist_ok=True)

# =========================================
# EXTRAER TEXTO
# =========================================

def extraer_texto_pdf(ruta_pdf):

    texto = ""

    documento = fitz.open(ruta_pdf)

    for pagina in documento:

        texto += pagina.get_text()

    return texto

# =========================================
# MAIN
# =========================================

def main():

    archivos = os.listdir(PDF_DIR)

    for archivo in archivos:

        if not archivo.endswith(".pdf"):
            continue

        ruta_pdf = os.path.join(

            PDF_DIR,
            archivo

        )

        texto = extraer_texto_pdf(

            ruta_pdf

        )

        nombre_txt = archivo.replace(

            ".pdf",
            ".txt"

        )

        ruta_txt = os.path.join(

            TXT_DIR,
            nombre_txt

        )

        with open(

            ruta_txt,
            "w",
            encoding="utf-8"

        ) as salida:

            salida.write(texto)

        print(

            f"✅ TXT generado: {ruta_txt}"

        )

# =========================================
# EJECUCIÓN
# =========================================

if __name__ == "__main__":

    main()
