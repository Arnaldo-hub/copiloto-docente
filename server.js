<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Copiloto Docente</title>

<style>
body{font-family:Arial;background:#f4f6f8;padding:40px}
.container{max-width:900px;margin:auto;background:white;padding:30px;border-radius:10px;box-shadow:0 0 15px rgba(0,0,0,0.1)}
label{font-weight:bold;margin-top:15px;display:block}
input,select{width:100%;padding:10px;margin-top:5px;border-radius:5px;border:1px solid #ccc}
button{margin-top:25px;width:100%;padding:12px;font-size:18px;border:none;border-radius:5px;background:#2c7be5;color:white;cursor:pointer}
#oaContainer{margin-top:10px}
#resultado{margin-top:40px;white-space:pre-wrap}
</style>
</head>
<body>

<div class="container">
<h1>Planificación de Clase</h1>

<label>Asignatura</label>
<input id="asignatura">

<label>Curso</label>
<input id="curso">

<label>Unidad</label>
<select id="unidad"></select>

<label>OA a trabajar</label>
<div id="oaContainer"></div>

<label>Duración (minutos)</label>
<input type="number" id="duracion">

<button onclick="generar()">Generar planificación</button>

<div id="resultado"></div>
</div>

<script>
// BASE CURRICULAR DEMO (puedes ampliarla luego)
const baseCurricular = {
  "Lenguaje y Comunicación": {
    "4 Básico": {
      "Unidad 1": ["OA1 Leer comprensivamente", "OA2 Escribir textos", "OA3 Comprender textos orales"],
      "Unidad 2": ["OA4 Producción escrita", "OA5 Uso de vocabulario"]
    }
  },
  "Matemática": {
    "4 Básico": {
      "Unidad 1": ["OA1 Números hasta 10.000", "OA2 Resolución de problemas"],
      "Unidad 2": ["OA3 Fracciones", "OA4 Representación gráfica"]
    }
  }
};

document.getElementById('asignatura').addEventListener('blur', cargarUnidades);
document.getElementById('curso').addEventListener('blur', cargarUnidades);
document.getElementById('unidad').addEventListener('change', cargarOA);

function cargarUnidades(){
  const asig = document.getElementById('asignatura').value;
  const curso = document.getElementById('curso').value;
  const unidadSelect = document.getElementById('unidad');
  unidadSelect.innerHTML = "";

  if(baseCurricular[asig] && baseCurricular[asig][curso]){
    const unidades = Object.keys(baseCurricular[asig][curso]);
    unidades.forEach(u=>{
      const opt = document.createElement('option');
      opt.value = u;
      opt.textContent = u;
      unidadSelect.appendChild(opt);
    });
    cargarOA();
  }
}

function cargarOA(){
  const asig = document.getElementById('asignatura').value;
  const curso = document.getElementById('curso').value;
  const unidad = document.getElementById('unidad').value;
  const oaDiv = document.getElementById('oaContainer');
  oaDiv.innerHTML = "";

  if(baseCurricular[asig] && baseCurricular[asig][curso]){
    const oas = baseCurricular[asig][curso][unidad];
    oas.forEach(oa=>{
      oaDiv.innerHTML += `<label><input type="checkbox" value="${oa}"> ${oa}</label>`;
    });
  }
}

async function generar(){
  const oas = [...document.querySelectorAll('#oaContainer input:checked')].map(x=>x.value).join(", ");

  const datos = {
    asignatura: document.getElementById('asignatura').value,
    curso: document.getElementById('curso').value,
    unidad: document.getElementById('unidad').value,
    oa: oas,
    duracion: document.getElementById('duracion').value
  };

  document.getElementById('resultado').innerHTML="Generando...";

  const res = await fetch('/copiloto/generar',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify(datos)
  });

  const json = await res.json();
  document.getElementById('resultado').innerHTML=json.resultado;
}
</script>

</body>
</html>
