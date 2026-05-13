// =========================================
// CURSOS
// =========================================

async function cargarCursos(){

    const asignatura =

    document.getElementById(
        "asignatura"
    ).value

    const cursoSelect =

    document.getElementById(
        "curso"
    )

    cursoSelect.innerHTML = ""

    try{

        const res = await fetch(

            `/api/cursos/${encodeURIComponent(asignatura)}`

        )

        const data = await res.json()

        data.cursos.forEach(curso => {

            cursoSelect.innerHTML += `

            <option value="${curso}">
                ${curso}
            </option>

            `

        })

        cargarUnidades()

    }catch(error){

        console.log(error)

    }

}

// =========================================
// UNIDADES
// =========================================

async function cargarUnidades(){

    const asignatura =

    document.getElementById(
        "asignatura"
    ).value

    const curso =

    document.getElementById(
        "curso"
    ).value

    const unidadSelect =

    document.getElementById(
        "unidad"
    )

    unidadSelect.innerHTML = ""

    try{

        const res = await fetch(

            `/api/unidades/${
                encodeURIComponent(asignatura)
            }/${
                encodeURIComponent(curso)
            }`

        )

        const data = await res.json()

        data.unidades.forEach(

            (unidad,index) => {

            unidadSelect.innerHTML += `

            <option value="${index+1}">
                ${unidad.nombre}
            </option>

            `

        })

        cargarOA()

    }catch(error){

        console.log(error)

    }

}

// =========================================
// OA
// =========================================

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

    const oaSelect =

    document.getElementById(
        "oa"
    )

    oaSelect.innerHTML = ""

    try{

        const res = await fetch(

            `/api/oa/${
                encodeURIComponent(asignatura)
            }/${
                encodeURIComponent(curso)
            }/${
                encodeURIComponent(unidad)
            }`

        )

        const data = await res.json()

        data.oa.forEach(oa => {

            oaSelect.innerHTML += `

            <option>

            ${oa.codigo}
            -
            ${oa.descripcion}

            </option>

            `

        })

    }catch(error){

        console.log(error)

    }

}

// =========================================
// INIT
// =========================================

window.onload = function(){

    cargarCursos()

}
