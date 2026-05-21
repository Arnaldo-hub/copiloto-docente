import os
from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def generar_imagen(prompt):

    try:

        respuesta = client.images.generate(

            model="gpt-image-1",

            prompt=f"""
Lámina educativa escolar.

Tema:
{prompt}

Estilo:
colorido
educativo
alta calidad
para estudiantes
""",

            size="1024x1024"
        )

        return {
            "ok": True,
            "url": respuesta.data[0].url
        }

    except Exception as e:

        print("ERROR IMAGEN:", str(e))

        return {
            "ok": False,
            "error": str(e)
        }
