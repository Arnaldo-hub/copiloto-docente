const express = require('express');
const path = require('path');

const app = express();
app.use(express.json());

// 👉 publicar carpeta public
app.use(express.static(path.join(__dirname, 'public')));

// ruta prueba
app.get('/ping', (req, res) => {
  res.send('Servidor vivo');
});

// endpoint del copiloto
app.post('/copiloto/generar', async (req, res) => {
  const { asignatura, curso, unidad, oa, duracion } = req.body;

  const prompt = `
Eres un experto docente chileno.

Genera una planificación de clase ORDENADA y clara.

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
`;

  try {
    const openai = new (require('openai'))({
      apiKey: process.env.OPENAI_API_KEY
    });

    const resp = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      messages: [{ role: "user", content: prompt }],
      temperature: 0.4
    });

    res.json({ resultado: resp.choices[0].message.content });
  } catch (e) {
    res.json({ resultado: "Error al generar planificación: " + e.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log("Servidor listo en puerto " + PORT));

