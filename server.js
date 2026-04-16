const express = require("express");
const path = require("path");
const OpenAI = require("openai");

const app = express();
app.use(express.json());

// Servir carpeta public
app.use(express.static(path.join(__dirname, "public")));

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Ruta de prueba
app.get("/ping", (req, res) => {
  res.send("Servidor vivo");
});

// RUTA QUE TU FORMULARIO USA
app.post("/copiloto/generar", async (req, res) => {
  try {
    const { asignatura, curso, unidad, oa, duracion } = req.body;

    const prompt = `
Eres un experto docente chileno.

Genera una planificación de clase ORDENADA, clara y profesional.

Datos:
Asignatura: ${asignatura}
Curso: ${curso}
Unidad: ${unidad}
OA: ${oa}
Duración: ${duracion} minutos

Estructura obligatoria:
1. Inicio
2. Desarrollo
3. Cierre
4. Evaluación
5. Materiales

No agregues saludos ni frases finales.
`;

    const completion = await client.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.7,
    });

    res.json({ resultado: completion.choices[0].message.content });
  } catch (error) {
    console.error(error);
    res.status(500).json({ resultado: "Error al generar planificación" });
  }
});

// IMPORTANTE: siempre al final
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Servidor iniciado en puerto " + PORT));
