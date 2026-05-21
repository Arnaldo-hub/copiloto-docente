import os
import time
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
Crear una lámina educativa.

Tema:
{prompt}

Alta calidad.
Para estudiantes.
Colorida.
Infografía.
"""

    }

    for _ in range(3):

        r = requests.post(

            API_URL,

            headers=headers,

            json=payload,

            timeout=180

        )

        if (

            "image"

            in r.headers.get(

                "content-type",

                ""

            )

        ):

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

        try:

            error = r.json()

        except:

            error = {}

        if (

            "estimated_time"

            in error

        ):

            time.sleep(

                error["estimated_time"]

            )

            continue

        raise Exception(

            str(error)

        )

    raise Exception(

        "No fue posible generar"

    )
