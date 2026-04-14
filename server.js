import express from "express";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
app.use(express.json());

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 👇 ESTO ES LO QUE FALTABA
app.use(express.static(path.join(__dirname, "public")));

// Ruta de prueba
app.get("/ping", (req, res) => {
  res.send("Servidor vivo");
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log("Servidor iniciado en puerto " + PORT);
});
