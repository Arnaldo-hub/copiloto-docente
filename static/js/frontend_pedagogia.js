
async function cargarCursos(){

    const asignatura =
    document.getElementById('asignatura').value

    const cursoSelect =
    document.getElementById('curso')

    cursoSelect.innerHTML = ''

    const res = await fetch(`/api/cursos/${asignatura}`)

    const cursos = await res.json()

    cursos.forEach(curso=>{

        cursoSelect.innerHTML += `
        <option>${curso}</option>
        `
    })

    cargarUnidades()
}

async function cargarUnidades(){

    const asignatura =
    document.getElementById('asignatura').value

    const curso =
    document.getElementById('curso').value

    const unidadSelect =
    document.getElementById('unidad')

    unidadSelect.innerHTML = ''

    const res = await fetch(`/api/unidades/${asignatura}/${curso}`)

    const unidades = await res.json()

    unidades.forEach(unidad=>{

        unidadSelect.innerHTML += `
        <option>${unidad.nombre}</option>
        `
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

    const oaSelect =
    document.getElementById('oa')

    oaSelect.innerHTML = ''

    const res = await fetch(`/api/oa/${asignatura}/${curso}/${unidad}`)

    const oa = await res.json()

    oa.forEach(item=>{

        oaSelect.innerHTML += `
        <option>${item.codigo} - ${item.descripcion}</option>
        `
    })
}

window.onload = function(){

    cargarCursos()
}
