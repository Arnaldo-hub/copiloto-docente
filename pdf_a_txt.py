import fitz
import os

PDF_DIR = "pdfs"
TXT_DIR = "txt"

os.makedirs(TXT_DIR, exist_ok=True)

def extraer_texto_pdf(ruta_pdf):

    texto = ""

    pdf = fitz.open(ruta_pdf)

    for pagina in pdf:

        texto += pagina.get_text()

    return texto

def main():

    archivos = os.listdir(PDF_DIR)

    print("📄 PDFs encontrados:")

    print(archivos)

    for archivo in archivos:

        if archivo.lower().endswith(".pdf"):

            ruta_pdf = os.path.join(
                PDF_DIR,
                archivo
            )

            print(f"Procesando: {archivo}")

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

            print(f"✅ TXT generado: {ruta_txt}")

if __name__ == "__main__":

    main()
