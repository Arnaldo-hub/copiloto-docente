async function cargarCursos(){

    const asignatura =
    document.getElementById(
        "asignatura"
    ).value

    const curso =
    document.getElementById(
        "curso"
    )

    curso.innerHTML = ""

    const res = await fetch(

        `/api/cursos/${asignatura}`

    )

    const data = await res.json()

    data.cursos.forEach(c => {

        curso.innerHTML += `

        <option value="${c}">
        ${c}
        </option>

        `

    })

    cargarUnidades()

}

async function cargarUnidades(){

    const asignatura =
    document.getElementById(
        "asignatura"
    ).value

    const curso =
    document.getElementById(
        "curso"
    ).value

    const unidad =
    document.getElementById(
        "unidad"
    )

    unidad.innerHTML = ""

    const res = await fetch(

        `/api/unidades/${asignatura}/${encodeURIComponent(curso)}`

    )

    const data = await res.json()

    data.unidades.forEach(u=>{

        unidad.innerHTML += `

        <option value="${u.nombre}">
        ${u.nombre}
        </option>

        `

    })

    cargarOA()

}

async function cargarOA(){

    const asignatura =
    document.getElementById(
        "asignatura"
    ).value

    const curso =
    document.getElementById(
        "curso"
    ).value

    const unidad =
    document.getElementById(
        "unidad"
    ).value

    const oa =
    document.getElementById(
        "oa"
    )

    oa.innerHTML = ""

    const res = await fetch(

        `/api/oa/${asignatura}/${encodeURIComponent(curso)}/${encodeURIComponent(unidad)}`

    )

    const data = await res.json()

    data.oa.forEach(o=>{

        oa.innerHTML += `

        <option>

        ${o.codigo} - ${o.descripcion}

        </option>

        `

    })

}

window.onload = function(){

    cargarCursos()

}
