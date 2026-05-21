import os
import requests


HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = (
"https://router.huggingface.co/nebius/v1/images/generations"
)


def generar_imagen(prompt):

    headers = {

        "Authorization":

        f"Bearer {HF_TOKEN}",

        "Content-Type":

        "application/json"

    }

    body = {

        "response_format":

        "b64_json",

        "prompt":

        f"""
Lámina educativa.

Tema:
{prompt}

Colorida.
Profesional.
Para estudiantes.
Alta calidad.
""",

        "model":

        "black-forest-labs/FLUX.1-schnell",

        "size":

        "1024x1024"

    }

    r = requests.post(

        API_URL,

        headers=headers,

        json=body,

        timeout=240

    )

    print(

        "HF",

        r.status_code

    )

    data = r.json()

    print(data)

    if r.status_code != 200:

        raise Exception(

            str(data)

        )

    import base64

    os.makedirs(

        "static",

        exist_ok=True

    )

    archivo = (

        "static/imagen_generada.png"

    )

    img = base64.b64decode(

        data["data"][0]["b64_json"]

    )

    with open(

        archivo,

        "wb"

    ) as f:

        f.write(img)

    return (

        "/static/imagen_generada.png"

    )
