import json

ARCHIVO = "data/matematica.json"

with open(
    ARCHIVO,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)

curso = data["1° Básico"]

for unidad in curso["unidades"]:

    for oa in unidad["oa"]:

        if "indicadores" not in oa:

            oa["indicadores"] = [
                "Demuestra comprensión del OA.",
                "Participa activamente en actividades.",
                "Aplica lo aprendido en ejercicios."
            ]

        if "habilidades" not in oa:

            oa["habilidades"] = [
                "Resolver problemas",
                "Comunicar",
                "Representar"
            ]

        if "actitudes" not in oa:

            oa["actitudes"] = [
                "Participa activamente.",
                "Persevera frente a desafíos.",
                "Respeta a sus compañeros."
            ]

        if "evaluacion" not in oa:

            oa["evaluacion"] = [
                "Observación directa",
                "Trabajo individual",
                "Resolución de actividades"
            ]

        if "actividades" not in oa:

            oa["actividades"] = {

                "inicio": [
                    "Activación de conocimientos previos.",
                    "Presentación del objetivo."
                ],

                "desarrollo": [
                    "Trabajo guiado.",
                    "Ejercicios prácticos.",
                    "Uso de material concreto."
                ],

                "cierre": [
                    "Síntesis de lo aprendido.",
                    "Ticket de salida."
                ]
            }

        if "adaptaciones_nee" not in oa:

            oa["adaptaciones_nee"] = [
                "Apoyo visual.",
                "Material concreto.",
                "Instrucciones segmentadas."
            ]

        if "recursos" not in oa:

            oa["recursos"] = [
                "Pizarra",
                "Guía de trabajo",
                "Material concreto"
            ]

with open(
    ARCHIVO,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        data,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    "✅ Matemática 1° Básico enriquecida"
)
