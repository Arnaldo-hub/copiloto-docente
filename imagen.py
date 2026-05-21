import os
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generar_imagen(prompt):

    try:

        respuesta = client.images.generate(

            model="gpt-image-1",

            prompt=prompt,

            size="512x512",
            quality="low"

        )

        return {

            "ok": True,

            "url":
            respuesta.data[0].url

        }

    except Exception as e:

        print("ERROR:", e)

        return {

            "ok": False,

            "error":
            str(e)

        }
