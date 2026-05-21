import os
import requests


HF_TOKEN = os.getenv("HF_TOKEN")


API_URL = (
"https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
)


def generar_imagen(prompt):

    headers = {

        "Authorization":

        f"Bearer {HF_TOKEN}"

    }

    payload = {

        "inputs":

        f"""
Crear lámina educativa.

Tema:
{prompt}

Estilo educativo.
Infografía.
Alta calidad.
Colorida.
"""

    }

    r = requests.post(

        API_URL,

        headers=headers,

        json=payload,

        timeout=240

    )

    print(

        "HF",

        r.status_code

    )

    if r.status_code != 200:

        print(r.text)

        raise Exception()

    os.makedirs(

        "static",

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

    return (

        "/static/imagen_generada.png"
    )
