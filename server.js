import express from "express";
import fetch from "node-fetch";

const app = express();
app.use(express.json());
app.use(express.static("public"));

const PORT = process.env.PORT || 3000;

app.post("/generar", async (req, res) => {
  try {
    const { prompt } = req.body;

    const response = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${process.env.OPENAI_API_KEY}`
      },
      body: JSON.stringify({
        model: "gpt-4o-mini",
        messages: [
          { role: "system", content: "Eres un experto docente chileno que genera planificaciones pedagógicas detalladas." },
          { role: "user", content: prompt }
        ],
        temperature: 0.7
      })
    });

    const data = await response.json();

    const texto = data.choices[0].message.content;

    res.json({ resultado: texto });

  } catch (error) {
    res.json({ resultado: "Error del servidor: " + error.message });
  }
});

app.listen(PORT, () => {
  console.log("Servidor activo en puerto " + PORT);
});
