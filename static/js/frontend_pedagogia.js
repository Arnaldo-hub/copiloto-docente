// =========================================
// FRONTEND PEDAGOGÍA
// COPILOTO DOCENTE
// =========================================

async function generarPedagogia(tipo){

    const resultado =
    document.getElementById('resultado')

    resultado.innerHTML =
    '⏳ Generando contenido pedagógico...'

    try{

        const asignatura =
        document.getElementById('asignatura').value

        const curso =
        document.getElementById('curso').value

        const unidad =
        document.getElementById('unidad').value

        const oa =
        document.getElementById('oa').value

        const res = await fetch('/api/pedagogia',{

            method:'POST',

            headers:{
                'Content-Type':'application/json'
            },

            body:JSON.stringify({

                tipo:tipo,

                asignatura:asignatura,

                curso:curso,

                unidad:unidad,

                oa:oa

            })

        })

        const data = await res.json()

        resultado.innerHTML = `

        <div style="white-space:pre-wrap;">

        ${data.resultado}

        </div>

        `

    }catch(error){

        console.log(error)

        resultado.innerHTML =

        'ERROR generando pedagogía.'
    }
}
