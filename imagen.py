import os
from openai import OpenAI


client = OpenAI(

api_key=

os.getenv(

"OPENAI_API_KEY"

)

)


def generar_imagen(

prompt

):

   r = client.images.generate(

model="gpt-image-1",

quality="low",

size="512x512",

prompt=f"""

Crear una lámina educativa.

Tema:

{prompt}

Estilo escolar.
Colorido.
Infografía.

"""

)

    import base64

    img = base64.b64decode(

        r.data[0].b64_json

    )

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

            img

        )

    return (

        "/static/imagen_generada.png"
    )
