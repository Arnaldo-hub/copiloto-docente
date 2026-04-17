const fs = require("fs");
const path = require("path");
const pdf = require("pdf-parse");

const carpetaPDF = "./bases_pdf"; // carpeta donde están los PDFs
const salidaJSON = "./base_curricular.json";

function limpiarTexto(texto) {
  return texto
    .replace(/\r/g, "")
    .replace(/\t/g, " ")
    .replace(/ +/g, " ")
    .split("\n");
}

function extraerOA(lineas) {
  const resultado = {};
  let unidadActual = null;

  for (let linea of lineas) {
    linea = linea.trim();

    if (/Unidad\s+\d+/i.test(linea)) {
      unidadActual = linea.match(/Unidad\s+\d+/i)[0];
      if (!resultado[unidadActual]) {
        resultado[unidadActual] = [];
      }
    }

    if (/OA\d+/i.test(linea) && unidadActual) {
      resultado[unidadActual].push(linea);
    }
  }

  return resultado;
}

async function procesarPDF(ruta) {
  const dataBuffer = fs.readFileSync(ruta);
  const data = await pdf(dataBuffer);
  const lineas = limpiarTexto(data.text);
  return extraerOA(lineas);
}

async function main() {
  const archivos = fs.readdirSync(carpetaPDF);
  const base = {};

  for (let archivo of archivos) {
    if (!archivo.endsWith(".pdf")) continue;

    console.log("Procesando:", archivo);

    const partes = archivo.replace(".pdf", "").split("_");
    // Ejemplo nombre: Matematica_4Basico.pdf
    const asignatura = partes[0];
    const curso = partes[1];

    const contenido = await procesarPDF(path.join(carpetaPDF, archivo));

    if (!base[asignatura]) base[asignatura] = {};
    base[asignatura][curso] = contenido;
  }

  fs.writeFileSync(salidaJSON, JSON.stringify(base, null, 2));
  console.log("\n✅ base_curricular.json generado correctamente");
}

main();
