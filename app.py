from flask import Flask, render_template, request, jsonify
import json
from openai import OpenAI

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

# 🔑 PON TU API KEY REAL
client = OpenAI(api_key="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")

# =========================
# CARGA BASE CURRICULAR
# =========================
with open("base_curricular_oficial.json", encoding="utf-8") as f:
    BASE = json.load(f)

# =========================
# RUTAS
# =========================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/base")
def base():
    return jsonify(BASE)


# 🔥 GENERAR PLANIFICACIÓN (IA PRO)
@app.route("/api/planificar", methods=["POST"])
def planificar():
    try:
        data = request.json

        asignatura = data['asignatura']
        curso = data['curso']
        unidad = data['unidad']
        oa_lista = data['oa']

        prompt = f"""
Actúa como experto en planificación docente del Ministerio de Educación de Chile.

Genera una planificación de clase de alto nivel pedagógico.

Asignatura: {asignatura}
Curso: {curso}
Unidad: {unidad}

Objetivos de Aprendizaje:
{chr(10).join(oa_lista)}

REQUISITOS:

- Definir UN objetivo claro
- Inicio con activación de conocimientos previos
- Desarrollo con actividades paso a paso
- Cierre con metacognición
- Evaluación con criterios observables
- Recursos concretos

Formato:

1. Objetivo de la clase
2. Inicio (10 min)
3. Desarrollo (25 min)
4. Cierre (5 min)
5. Evaluación
6. Recursos
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        return jsonify({
            "plan": response.choices[0].message.content
        })

    except Exception as e:
        print("🔥 ERROR IA:", e)
        return jsonify({"plan": "❌ Error al generar planificación"})


# 🔥 GENERAR PDF
@app.route("/api/pdf", methods=["POST"])
def generar_pdf():
    try:
        data = request.json
        texto = data["contenido"]

        file_path = "planificacion.pdf"

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        contenido = []
        for linea in texto.split("\n"):
            contenido.append(Paragraph(linea, styles["Normal"]))

        doc.build(contenido)

        return jsonify({"ok": True})

    except Exception as e:
        print("🔥 ERROR PDF:", e)
        return jsonify({"ok": False})


# =========================
if __name__ == "__main__":
    app.run(debug=True)