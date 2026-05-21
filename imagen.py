import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = (
    "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
)

def generar_imagen(prompt):

    headers = {

        "Authorization":

        f"Bearer {HF_TOKEN}"

    }

    payload = {

        "inputs":

        f"""
Lámina educativa profesional:

{prompt}

Alta calidad.
Formato escolar.
Colorido.
Infografía.
"""

    }

    r = requests.post(

        API_URL,

        headers=headers,

        json=payload,

        timeout=120

    )

    if r.status_code != 200:

        raise Exception(

            r.text

        )

    carpeta = "static"

    os.makedirs(

        carpeta,

        exist_ok=True

    )

    ruta = (

        "static/imagen_generada.png"

    )

    with open(

        ruta,

        "wb"

    ) as f:

        f.write(

            r.content

        )

    return "/static/imagen_generada.png"
