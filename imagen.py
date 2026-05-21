import os
from openai import OpenAI


client = OpenAI(

api_key=

os.getenv(

"OPENAI_API_KEY"

)

)


import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generar_imagen(prompt):

    try:

        r = client.images.generate(

            model="gpt-image-1",

            prompt=f"""
Crear una lámina educativa.

Tema:
{prompt}

Estilo:
infografía escolar,
colores suaves,
alta legibilidad.
""",

            size="512x512",
            quality="low"
        )

        return {

            "ok": True,

            "url":
            r.data[0].url

        }

    except Exception as e:

        print(e)

        return {

            "ok": False,

            "error": str(e)

        }

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
