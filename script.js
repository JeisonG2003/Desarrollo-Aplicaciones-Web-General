const formulario = document.getElementById("formCultivo");
const listaCultivos = document.getElementById("listaCultivos");
const mensaje = document.getElementById("mensaje");
const totalRegistros = document.getElementById("totalRegistros");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const errorNombre = document.getElementById("errorNombre");
const errorDescripcion = document.getElementById("errorDescripcion");
const errorCategoria = document.getElementById("errorCategoria");

let contador = 0;

// VALIDAR NOMBRE

function validarNombre() {

    if (nombre.value.trim() === "") {

        errorNombre.textContent = "El nombre del cultivo es obligatorio.";

        nombre.classList.remove("is-valid");
        nombre.classList.add("is-invalid");

        return false;

    }

    if (nombre.value.trim().length < 3) {

        errorNombre.textContent = "Debe contener al menos 3 caracteres.";

        nombre.classList.remove("is-valid");
        nombre.classList.add("is-invalid");

        return false;

    }

    errorNombre.textContent = "";

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    return true;

}

// VALIDAR DESCRIPCIÓN

function validarDescripcion() {

    if (descripcion.value.trim() === "") {

        errorDescripcion.textContent = "La descripción es obligatoria.";

        descripcion.classList.remove("is-valid");
        descripcion.classList.add("is-invalid");

        return false;

    }

    if (descripcion.value.trim().length < 10) {

        errorDescripcion.textContent = "La descripción debe contener al menos 10 caracteres.";

        descripcion.classList.remove("is-valid");
        descripcion.classList.add("is-invalid");

        return false;

    }

    errorDescripcion.textContent = "";

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    return true;

}

// VALIDAR CATEGORÍA

function validarCategoria() {

    if (categoria.value === "") {

        errorCategoria.textContent = "Seleccione una categoría.";

        categoria.classList.remove("is-valid");
        categoria.classList.add("is-invalid");

        return false;

    }

    errorCategoria.textContent = "";

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    return true;

}

// EVENTOS EN TIEMPO REAL

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

// REGISTRAR CULTIVO

formulario.addEventListener("submit", function (event) {

    event.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Corrija los campos marcados antes de registrar el cultivo.
            </div>
        `;

        return;

    }

    const cultivo = document.createElement("div");

    cultivo.className = "card p-3 mb-3 shadow";

    cultivo.innerHTML = `
        <h5>${nombre.value}</h5>

        <p>
            <strong>Categoría:</strong> ${categoria.value}
        </p>

        <p>${descripcion.value}</p>
    `;

    const botonEliminar = document.createElement("button");

    botonEliminar.textContent = "Eliminar registro";
    botonEliminar.className = "btn btn-danger mt-2";

    botonEliminar.addEventListener("click", function () {

        cultivo.remove();

        contador--;

        totalRegistros.textContent = contador;

        mensaje.innerHTML = `
            <div class="alert alert-warning">
                El registro fue eliminado correctamente.
            </div>
        `;

    });

    cultivo.appendChild(botonEliminar);

    listaCultivos.appendChild(cultivo);

    contador++;

    totalRegistros.textContent = contador;

    mensaje.innerHTML = `
        <div class="alert alert-success">
            El cultivo fue registrado correctamente.
        </div>
    `;

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

    errorNombre.textContent = "";
    errorDescripcion.textContent = "";
    errorCategoria.textContent = "";

});