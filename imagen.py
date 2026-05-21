import os
import time
import requests


HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = (
    "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"
)


def generar_imagen(prompt):

    headers = {

        "Authorization":

        f"Bearer {HF_TOKEN}",

        "Content-Type":

        "application/json"

    }

    body = {

        "inputs":

        f"""
Crear una lámina educativa.

Tema:
{prompt}

Estilo:
infografía educativa.
colores vivos.
alta calidad.
"""

    }

    try:

        r = requests.post(

            API_URL,

            headers=headers,

            json=body,

            timeout=240

        )

        print(
            "HF:",
            r.status_code
        )

        print(
            r.text[:500]
        )

        if r.status_code != 200:

            raise Exception(
                r.text
            )

        os.makedirs(

            "static",

            exist_ok=True

        )

        archivo = (

            "static/imagen_generada.png"

        )

        with open(

            archivo,

            "wb"

        ) as f:

            f.write(

                r.content

            )

        return (

            "/static/imagen_generada.png"

        )

    except Exception as e:

        print(e)

        raise
