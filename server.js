const express = require('express');
const path = require('path');

const app = express();
app.use(express.json());

// 🔥 RUTA ABSOLUTA CORRECTA PARA RENDER
const publicPath = path.resolve(__dirname, 'public');
app.use(express.static(publicPath));

app.get('/ping', (req, res) => {
  res.send('Servidor vivo');
});

app.get('/testjson', (req, res) => {
  res.sendFile(path.join(publicPath, 'base_curricular.json'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log('Servidor usando carpeta pública en:', publicPath);
});
