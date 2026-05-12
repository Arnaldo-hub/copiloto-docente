<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0">

<title>
Copiloto Docente IA
</title>

<style>

body{
    margin:0;
    background:#03133b;
    color:white;
    font-family:Arial;
}

.container{
    display:grid;
    grid-template-columns:320px 420px 1fr;
    min-height:100vh;
}

.panel{
    padding:20px;
    border-right:1px solid rgba(255,255,255,0.1);
}

.card{
    background:#1b2b55;
    padding:20px;
    border-radius:16px;
    margin-bottom:20px;
}

textarea,
select{
    width:100%;
    padding:14px;
    border-radius:12px;
    border:none;
    margin-bottom:15px;
    font-size:18px;
}

button{
    width:100%;
    padding:16px;
    border:none;
    border-radius:12px;
    background:#22c55e;
    color:white;
    font-size:18px;
    font-weight:bold;
    cursor:pointer;
    margin-bottom:15px;
}

button:hover{
    opacity:0.9;
}

img{
    max-width:100%;
    border-radius:12px;
    margin-top:15px;
}

#resultado,
#historial{
    background:#1b2b55;
    padding:20px;
    border-radius:16px;
    min-height:250px;
    overflow:auto;
}

@media(max-width:1200px){

    .container{
        grid-template-columns:1fr;
    }

    .panel{
        border-right:none;
        border-bottom:1px solid rgba(255,255,255,0.1);
    }
}

</style>

</head>

<body>

<div class="container">

<!-- ================================= -->
<!-- CHAT IA -->
<!-- ================================= -->

<div class="panel">

<h1>
🧠 Chat Docente IA
</h1>

<div class="card">

<textarea
id="preguntaIA"
rows="8"
placeholder="Escribe una pregunta pedagógica...">
</textarea>

<button onclick="preguntarIA()">
💬 Preguntar
</button>

<div id="respuestaIA"
style="margin-top:20px;">
</div>

</div>

</div>

<!-- ================================= -->
<!-- CONTEXTO PEDAGÓGICO -->
<!-- ================================= -->

<div class="panel">

<h1>
📚 Contexto Pedagógico
</h1>

<div class="card">

<select id="asignatura"
onchange="cargarCursos()">

<option value="matematica">
Matemática
</option>

<option value="lenguaje">
Lenguaje y Comunicación
</option>

<option value="ciencias">
Ciencias Naturales
</option>

<option value="historia">
Historia y Geografía
</option>

</select>

<select id="curso"
onchange="cargarUnidades()">
</select>

<select id="unidad"
onchange="cargarOA()">
</select>

<select id="oa">
</select>

</div>

<!-- ================================= -->
<!-- MÓDULOS -->
<!-- ================================= -->

<div class="card">

<label>

<input
type="checkbox"
id="check_objetivos">

🎯 Objetivos

</label>

<br><br>

<label>

<input
type="checkbox"
id="check_indicadores">

📊 Indicadores

</label>

<br><br>

<label>

<input
type="checkbox"
id="check_habilidades">

🧠 Habilidades

</label>

<br><br>

<label>

<input
type="checkbox"
id="check_actitudes">

🤝 Actitudes

</label>

<br><br>

<label>

<input
type="checkbox"
id="check_nee">

♿ Adaptaciones NEE

</label>

<br><br>

<label>

<input
type="checkbox"
id="check_evaluacion">

📝 Evaluaciones

</label>

<br><br>

<button onclick="generarPlanificacion()">

🚀 Generar Planificación

</button>

</div>

</div>

<!-- ================================= -->
<!-- RESULTADO -->
<!-- ================================= -->

<div class="panel">

<h1>
📄 Resultado IA
</h1>

<div id="resultado">

Resultado pedagógico aparecerá aquí.

</div>

</div>

</div>

<!-- ================================= -->
<!-- CHAT IA -->
<!-- ================================= -->

<script>

async function preguntarIA(){

    const pregunta =

    document.getElementById(
        'preguntaIA'
    ).value

    const respuesta =

    document.getElementById(
        'respuestaIA'
    )

    respuesta.innerText =
    '⏳ Pensando...'

    try{

        const res = await fetch(

            '/api/chat',

            {

                method:'POST',

                headers:{
                    'Content-Type':
                    'application/json'
                },

                body:JSON.stringify({

                    pregunta:
                    pregunta

                })

            }

        )

        const data =
        await res.json()

        respuesta.innerText =
        data.respuesta

    }catch(error){

        console.log(error)

        respuesta.innerText =
        'ERROR conectando IA'
    }
}

// =========================================
// CURSOS
// =========================================

async function cargarCursos(){

    const asignatura =

    document.getElementById(
        'asignatura'
    ).value

    const cursoSelect =

    document.getElementById(
        'curso'
    )

    cursoSelect.innerHTML = ''

    const res = await fetch(

        `/api/cursos/${asignatura}`

    )

    const cursos = await res.json()

    cursos.forEach(curso => {

        cursoSelect.innerHTML += `

        <option>

        ${curso}

        </option>

        `
    })

    cargarUnidades()
}

// =========================================
// UNIDADES
// =========================================

async function cargarUnidades(){

    const asignatura =

    document.getElementById(
        'asignatura'
    ).value

    const curso =

    document.getElementById(
        'curso'
    ).value

    const unidadSelect =

    document.getElementById(
        'unidad'
    )

    unidadSelect.innerHTML = ''

    const res = await fetch(

        `/api/unidades/${asignatura}/${curso}`

    )

    const unidades = await res.json()

    unidades.forEach(unidad => {

        unidadSelect.innerHTML += `

        <option>

        ${unidad.nombre}

        </option>

        `
    })

    cargarOA()
}

// =========================================
// OA
// =========================================

async function cargarOA(){

    const asignatura =

    document.getElementById(
        'asignatura'
    ).value

    const curso =

    document.getElementById(
        'curso'
    ).value

    const unidad =

    document.getElementById(
        'unidad'
    ).value

    const oaSelect =

    document.getElementById(
        'oa'
    )

    oaSelect.innerHTML = ''

    const res = await fetch(

        `/api/oa/${asignatura}/${curso}/${unidad}`

    )

    const oa = await res.json()

    oa.forEach(item => {

        oaSelect.innerHTML += `

        <option>

        ${item.codigo} -
        ${item.descripcion}

        </option>

        `
    })
}

// =========================================
// INICIO
// =========================================

cargarCursos()

</script>

<!-- ================================= -->
<!-- JS PEDAGOGÍA -->
<!-- ================================= -->

<script src="/static/js/frontend_pedagogia.js"></script>

</body>
</html>
