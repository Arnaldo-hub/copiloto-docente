import express from "express";

const app = express();
app.use(express.json());
app.use(express.static("public"));

app.get("/ping", (req, res) => {
  res.send("Servidor vivo");
});

app.post("/copiloto/generar", async (req, res) => {
  try {
    const { nombre, asignatura, tema } = req.body;

    const prompt = `
Eres el Copiloto Docente.
Crea una planificación de clase para:

Docente: ${nombre}
Asignatura: ${asignatura}
Tema: ${tema}

Incluye:
- Inicio
- Desarrollo
- Cierre
- Evaluación
`;

    const response = await fetch("https://api.openai.com/v1/responses", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-4.1",
        input: prompt,
      }),
    });

    const data = await response.json();

    // 👇 ESTA ES LA FORMA CORRECTA
    const texto = data.output[0].content[0].text;

    res.json({ resultado: texto });

  } catch (error) {
    console.error(error);
    res.status(500).json({ resultado: "Error al generar la planificación" });
  }
});

app.listen(3000, () => {
  console.log("Servidor iniciado en puerto 3000");
});
