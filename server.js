import express from "express";

const app = express();
app.use(express.json());
app.use(express.static("public"));

app.get("/ping", (req, res) => {
  res.send("Servidor vivo");
});

app.post("/copiloto/generar", async (req, res) => {
  const { nombre, asignatura, tema } = req.body;

  const prompt = `
Eres el Copiloto Docente.
Crea una planificación de clase para:
Docente: ${nombre}
Asignatura: ${asignatura}
Tema: ${tema}
Incluye inicio, desarrollo y cierre.
`;

  try {
    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-4.1",
        input: prompt
      })
    });

    const data = await response.json();
    res.json({ resultado: data.output_text });
  } catch (error) {
    res.status(500).json({ error: "Error al generar respuesta" });
  }
});

app.listen(3000, () => {
  console.log("Servidor iniciado en puerto 3000");
});
