import os
import base64
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generar_imagen(prompt):

    try:

        respuesta = client.images.generate(

            model="gpt-image-1",

            prompt=prompt,

            size="1024x1024",

            quality="low"

        )

        # GPT Image devuelve base64
        imagen_base64 = respuesta.data[0].b64_json

        return {

            "ok": True,

            "imagen": (
                "data:image/png;base64,"
                + imagen_base64
            )

        }

    except Exception as e:

        print("ERROR:", str(e))

        return {

            "ok": False,

            "error": str(e)

        }
