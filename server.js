import express from "express";
import OpenAI from "openai";

const app = express();
app.use(express.json());
app.use(express.static("public"));

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post("/copiloto/generar", async (req, res) => {
  try {
    const { asignatura, curso, unidad, oa, duracion } = req.body;

    const prompt = `
Eres un experto planificador pedagógico chileno.

PROHIBIDO:
- No saludar
- No despedirse
- No hacer preguntas
- No agregar frases como "Por supuesto", "Aquí tienes", "¿Deseas modificar algo?"
- No agregar introducciones ni cierres conversacionales

OBLIGATORIO:
- Entregar directamente la planificación.
- Formato claro, profesional y ordenado.
- Usar títulos y subtítulos.
- Redactar como documento pedagógico formal.

Datos de la clase:
Asignatura: ${asignatura}
Curso: ${curso}
Unidad: ${unidad}
OA: ${oa}
Duración: ${duracion} minutos
`;

    const response = await client.responses.create({
      model: "gpt-5-nano",
      input: prompt,
    });

    const texto = response.output_text;

    res.json({ resultado: texto });
  } catch (error) {
    console.error(error);
    res.status(500).json({ resultado: "Error al generar planificación" });
  }
});

app.get("/ping", (req, res) => {
  res.send("Servidor vivo");
});

app.listen(process.env.PORT || 3000, () => {
  console.log("Servidor iniciado");
});
