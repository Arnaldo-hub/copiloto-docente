import os
from openai import OpenAI


# ==========================================
# CLIENTE OPENAI
# ==========================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# ==========================================
# GENERAR IMAGEN
# ==========================================

def generar_imagen(prompt):

    try:

        respuesta = client.images.generate(

            model="gpt-image-1",

            prompt=f"""
Crear una imagen educativa.

Tema:
{prompt}

Estilo:
infografía educativa
colores atractivos
para estudiantes
alta calidad
""",

            size="1024x1024",

            quality="medium"

        )

        return {

            "ok": True,

            "url":
            respuesta.data[0].url

        }

    except Exception as e:

        print(
            "ERROR IMAGEN:",
            str(e)
        )

        return {

            "ok": False,

            "error":
            str(e)

        }
