async function cargarCursos() {

    try {

        const asignatura =
        document.getElementById(
            "asignatura"
        ).value;

        const curso =
        document.getElementById(
            "curso"
        );

        curso.innerHTML = "";

        const res = await fetch(

            `/api/cursos/${encodeURIComponent(asignatura)}`

        );

        const data = await res.json();

        if (!data.cursos) {

            console.log(
                "No hay cursos"
            );

            return;
        }

        data.cursos.forEach(c => {

            curso.innerHTML += `

            <option value="${c}">
            ${c}
            </option>

            `;

        });

        await cargarUnidades();

    } catch (error) {

        console.log(
            "ERROR cursos:",
            error
        );

    }

}

async function cargarUnidades() {

    try {

        const asignatura =
        document.getElementById(
            "asignatura"
        ).value;

        const curso =
        document.getElementById(
            "curso"
        ).value;

        const unidad =
        document.getElementById(
            "unidad"
        );

        unidad.innerHTML = "";

        const url =

        `/api/unidades/${encodeURIComponent(asignatura)}/${encodeURIComponent(curso)}`;

        console.log(
            "Cargando unidades:",
            url
        );

        const res = await fetch(url);

        const data = await res.json();

        console.log(
            "UNIDADES:",
            data
        );

        if (!data.unidades) {

            return;
        }

        data.unidades.forEach(u => {

            unidad.innerHTML += `

            <option value="${u.nombre}">
            ${u.nombre}
            </option>

            `;

        });

        await cargarOA();

    } catch (error) {

        console.log(
            "ERROR unidades:",
            error
        );

    }

}

async function cargarOA() {

    try {

        const asignatura =
        document.getElementById(
            "asignatura"
        ).value;

        const curso =
        document.getElementById(
            "curso"
        ).value;

        const unidad =
        document.getElementById(
            "unidad"
        ).value;

        const oa =
        document.getElementById(
            "oa"
        );

        oa.innerHTML = "";

        const url =

        `/api/oa/${encodeURIComponent(asignatura)}/${encodeURIComponent(curso)}/${encodeURIComponent(unidad)}`;

        console.log(
            "Cargando OA:",
            url
        );

        const res = await fetch(url);

        const data = await res.json();

        console.log(
            "OA:",
            data
        );

        if (!data.oa) {

            return;
        }

        data.oa.forEach(o => {

            oa.innerHTML += `

            <option>

            ${o.codigo} - ${o.descripcion}

            </option>

            `;

        });

    } catch (error) {

        console.log(
            "ERROR OA:",
            error
        );

    }

}

window.onload = function () {

    cargarCursos();

};
