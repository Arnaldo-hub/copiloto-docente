const express = require("express");
const path = require("path");
const OpenAI = require("openai");

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 👉 Servir el index.html correctamente
app.use(express.static(path.join(__dirname)));

// 👉 Ruta principal (esto quita el "Cannot GET /")
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "index.html"));
});

// 👉 Ruta que usa el formulario
app.post("/generar", async (req, res) => {
  try {
    const openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY,
    });

    const { tema, nivel, objetivo } = req.body;

    const prompt = `
    Crea una aplicación educativa con:
    Tema: ${tema}
    Nivel: ${nivel}
    Objetivo: ${objetivo}
    `;

    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: prompt }],
    });

    res.send(completion.choices[0].message.content);
  } catch (error) {
    console.error(error);
    res.status(500).send("Error al generar la aplicación");
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Servidor iniciado"));
