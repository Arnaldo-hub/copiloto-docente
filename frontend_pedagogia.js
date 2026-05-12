// =========================================
// FRONTEND PEDAGOGÍA
// COPILOTO DOCENTE
// =========================================

async function generarPlanificacion(){

    const resultado =
    document.getElementById('resultado')

    resultado.innerHTML =
    '⏳ Generando planificación...'

    try{

        // =====================================
        // CONTEXTO PEDAGÓGICO
        // =====================================

        const asignatura =
        document.getElementById('asignatura').value

        const curso =
        document.getElementById('curso').value

        const unidad =
        document.getElementById('unidad').value

        const oa =
        document.getElementById('oa').value

        // =====================================
        // CHECKBOXES
        // =====================================

        const checks = {

            objetivos:
            document.getElementById(
                'check_objetivos'
            ).checked,

            indicadores:
            document.getElementById(
                'check_indicadores'
            ).checked,

            habilidades:
            document.getElementById(
                'check_habilidades'
            ).checked,

            actitudes:
            document.getElementById(
                'check_actitudes'
            ).checked,

            nee:
            document.getElementById(
                'check_nee'
            ).checked,

            evaluacion:
            document.getElementById(
                'check_evaluacion'
            ).checked

        }

        // =====================================
        // RESULTADO FINAL
        // =====================================

        let contenidoFinal = ''

        // =====================================
        // OBJETIVOS
        // =====================================

        if(checks.objetivos){

            const res =
            await fetch('/api/pedagogia',{

                method:'POST',

                headers:{
                    'Content-Type':
                    'application/json'
                },

                body:JSON.stringify({

                    tipo:'objetivos',

                    asignatura:
                    asignatura,

                    curso:
                    curso,

                    unidad:
                    unidad,

                    oa:
                    oa

                })

            })

            const data =
            await res.json()

            contenidoFinal += `

            <h2>
            🎯 Objetivos
            </h2>

            <div style="white-space:pre-wrap;">
            ${data.resultado}
            </div>

            <hr>

            `
        }

        // =====================================
        // INDICADORES
        // =====================================

        if(checks.indicadores){

            const res =
            await fetch('/api/pedagogia',{

                method:'POST',

                headers:{
                    'Content-Type':
                    'application/json'
                },

                body:JSON.stringify({

                    tipo:'indicadores',

                    asignatura:
                    asignatura,

                    curso:
                    curso,

                    unidad:
                    unidad,

                    oa:
                    oa

                })

            })

            const data =
            await res.json()

            contenidoFinal += `

            <h2>
            📊 Indicadores
            </h2>

            <div style="white-space:pre-wrap;">
            ${data.resultado}
            </div>

            <hr>

            `
        }

        // =====================================
        // HABILIDADES
        // =====================================

        if(checks.habilidades){

            const res =
            await fetch('/api/pedagogia',{

                method:'POST',

                headers:{
                    'Content-Type':
                    'application/json'
                },

                body:JSON.stringify({

                    tipo:'habilidades',

                    asignatura:
                    asignatura,

                    curso:
                    curso,

                    unidad:
                    unidad,

                    oa:
                    oa

                })

            })

            const data =
            await res.json()

            contenidoFinal += `

            <h2>
            🧠 Habilidades
            </h2>

            <div style="white-space:pre-wrap;">
            ${data.resultado}
            </div>

            <hr>

            `
        }

        // =====================================
        // ACTITUDES
        // =====================================

        if(checks.actitudes){

            const res =
            await fetch('/api/pedagogia',{

                method:'POST',

                headers:{
                    'Content-Type':
                    'application/json'
                },

                body:JSON.stringify({

                    tipo:'actitudes',

                    asignatura:
                    asignatura,

                    curso:
                    curso,

                    unidad:
                    unidad,

                    oa:
                    oa

                })

            })

            const data =
            await res.json()

            contenidoFinal += `

            <h2>
            🤝 Actitudes
            </h2>

            <div style="white-space:pre-wrap;">
            ${data.resultado}
            </div>

            <hr>

            `
        }

        // =====================================
        // NEE
        // =====================================

        if(checks.nee){

            const res =
            await fetch('/api/pedagogia',{

                method:'POST',

                headers:{
                    'Content-Type':
                    'application/json'
                },

                body:JSON.stringify({

                    tipo:'nee',

                    asignatura:
                    asignatura,

                    curso:
                    curso,

                    unidad:
                    unidad,

                    oa:
                    oa

                })

            })

            const data =
            await res.json()

            contenidoFinal += `

            <h2>
            ♿ Adaptaciones NEE
            </h2>

            <div style="white-space:pre-wrap;">
            ${data.resultado}
            </div>

            <hr>

            `
        }

        // =====================================
        // EVALUACIÓN
        // =====================================

        if(checks.evaluacion){

            const res =
            await fetch('/api/pedagogia',{

                method:'POST',

                headers:{
                    'Content-Type':
                    'application/json'
                },

                body:JSON.stringify({

                    tipo:'evaluacion',

                    asignatura:
                    asignatura,

                    curso:
                    curso,

                    unidad:
                    unidad,

                    oa:
                    oa

                })

            })

            const data =
            await res.json()

            contenidoFinal += `

            <h2>
            📝 Evaluaciones
            </h2>

            <div style="white-space:pre-wrap;">
            ${data.resultado}
            </div>

            <hr>

            `
        }

        // =====================================
        // MOSTRAR RESULTADO
        // =====================================

        resultado.innerHTML =
        contenidoFinal

    }catch(error){

        console.log(error)

        resultado.innerHTML =
        'ERROR generando planificación.'
    }
}
