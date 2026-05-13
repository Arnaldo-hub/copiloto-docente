async function cargarUnidades(){

    const asignatura =
    document.getElementById('asignatura').value

    const curso =
    document.getElementById('curso').value

    const unidad =
    document.getElementById('unidad')

    unidad.innerHTML = ''

    const res = await fetch('/api/unidades',{

        method:'POST',

        headers:{
            'Content-Type':'application/json'
        },

        body:JSON.stringify({
            asignatura,
            curso
        })

    })

    const data = await res.json()

    data.forEach(item=>{

        const option =
        document.createElement('option')

        option.value =
        item.nombre

        option.textContent =
        item.nombre

        unidad.appendChild(option)

    })

    cargarOA()
}

async function cargarOA(){

    const asignatura =
    document.getElementById('asignatura').value

    const curso =
    document.getElementById('curso').value

    const unidad =
    document.getElementById('unidad').value

    const oa =
    document.getElementById('oa')

    oa.innerHTML = ''

    const res = await fetch('/api/oa',{

        method:'POST',

        headers:{
            'Content-Type':'application/json'
        },

        body:JSON.stringify({
            asignatura,
            curso,
            unidad
        })

    })

    const data = await res.json()

    data.forEach(item=>{

        const option =
        document.createElement('option')

        option.value =
        item.codigo

        option.textContent =
        item.codigo + ' - ' + item.descripcion

        oa.appendChild(option)

    })

}

async function generarPlanificacion(){

    const resultado =
    document.getElementById('resultado')

    resultado.innerHTML =
    '⏳ Generando planificación...'

    const res = await fetch('/api/pedagogia',{

        method:'POST',

        headers:{
            'Content-Type':'application/json'
        },

        body:JSON.stringify({

            asignatura:
            document.getElementById('asignatura').value,

            curso:
            document.getElementById('curso').value,

            unidad:
            document.getElementById('unidad').value,

            oa:
            document.getElementById('oa').value

        })

    })

    const data = await res.json()

    resultado.innerHTML =
    `<pre>${data.resultado}</pre>`
}

window.onload = ()=>{
    cargarUnidades()
}
