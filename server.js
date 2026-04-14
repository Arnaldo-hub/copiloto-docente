const express = require('express');
const path = require('path');
const OpenAI = require('openai');

const app = express();
const BASE = '/copiloto';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Servir estáticos
app.use(BASE, express.static(path.join(__dirname, 'public')));

// Página principal
app.get(BASE, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Generar planificación
app.post(BASE + '/generar', async (req, res) => {
  try {
    const { asignatura, curso, unidad, mes } = req.body;

    const prompt = `
Asignatura: ${asignatura}
Curso: ${curso}
Unidad: ${unidad}
Mes: ${mes}
Genera la planificación mensual completa.
`;

    const response = await openai.responses.create({
      model: 'gpt-5.4',
      input: prompt,
      max_output_tokens: 2000
    });

    res.send(`
      <h2>Planificación Generada</h2>
      <pre>${response.output_text}</pre>
      <br><a href="/copiloto">Volver</a>
    `);

  } catch (error) {
    res.send("Error: " + error.message);
  }
});

module.exports = app;
