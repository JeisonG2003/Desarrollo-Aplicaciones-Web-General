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

// Bootstrap
const spinner = document.getElementById("spinner");
const modalInformacion = new bootstrap.Modal(
    document.getElementById("modalInformacion")
);

// Arreglo que almacenará los cultivos
let cultivos = [];

// ===============================
// VALIDACIONES
// ===============================

function validarNombre() {

    if (nombre.value.trim() === "") {

        errorNombre.textContent = "El nombre del cultivo es obligatorio.";
        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        return false;

    }

    if (nombre.value.trim().length < 3) {

        errorNombre.textContent = "Debe contener al menos 3 caracteres.";
        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        return false;

    }

    errorNombre.textContent = "";
    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    return true;

}

function validarDescripcion() {

    if (descripcion.value.trim() === "") {

        errorDescripcion.textContent = "La descripción es obligatoria.";
        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        return false;

    }

    if (descripcion.value.trim().length < 10) {

        errorDescripcion.textContent = "La descripción debe contener al menos 10 caracteres.";
        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        return false;

    }

    errorDescripcion.textContent = "";
    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    return true;

}

function validarCategoria() {

    if (categoria.value === "") {

        errorCategoria.textContent = "Seleccione una categoría.";
        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        return false;

    }

    errorCategoria.textContent = "";
    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    return true;

}

// ===============================
// EVENTOS
// ===============================

nombre.addEventListener("input", validarNombre);
nombre.addEventListener("blur", validarNombre);

descripcion.addEventListener("input", validarDescripcion);
descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);
categoria.addEventListener("blur", validarCategoria);

// ===============================
// RENDERIZAR CULTIVOS
// ===============================

function renderizarCultivos() {

    listaCultivos.innerHTML = "";

    if (cultivos.length === 0) {

        listaCultivos.innerHTML = `
            <div class="alert alert-info">
                Todavía no existen cultivos registrados.
            </div>
        `;

        totalRegistros.textContent = "0";

        return;

    }

    cultivos.forEach(function(cultivo, indice) {

        const tarjeta = document.createElement("div");

        tarjeta.className = "card shadow p-3 mb-3";

        tarjeta.innerHTML = `
            <h5>${cultivo.nombre}</h5>

            <p>
                <strong>Categoría:</strong>
                ${cultivo.categoria}
            </p>

            <p>${cultivo.descripcion}</p>
        `;

        const botonEliminar = document.createElement("button");

        botonEliminar.textContent = "Eliminar registro";
        botonEliminar.className = "btn btn-danger mt-2";

        botonEliminar.addEventListener("click", function () {

            cultivos.splice(indice, 1);

            renderizarCultivos();

            mensaje.innerHTML = `
                <div class="alert alert-warning">
                    Registro eliminado correctamente.
                </div>
            `;

        });

        tarjeta.appendChild(botonEliminar);

        listaCultivos.appendChild(tarjeta);

    });

    totalRegistros.textContent = cultivos.length;

}

// ===============================
// REGISTRAR CULTIVO
// ===============================

formulario.addEventListener("submit", function(event) {

    event.preventDefault();

    const nombreValido = validarNombre();
    const descripcionValida = validarDescripcion();
    const categoriaValida = validarCategoria();

    if (!nombreValido || !descripcionValida || !categoriaValida) {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Corrija los errores antes de registrar el cultivo.
            </div>
        `;

        return;

    }

const nuevoCultivo = {

    nombre: nombre.value.trim(),
    descripcion: descripcion.value.trim(),
    categoria: categoria.value

};

spinner.classList.remove("d-none");

setTimeout(function () {

    cultivos.push(nuevoCultivo);

    renderizarCultivos();

    spinner.classList.add("d-none");

    mensaje.innerHTML = `
        <div class="alert alert-success">
            Cultivo registrado correctamente.
        </div>
    `;

    modalInformacion.show();

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

    errorNombre.textContent = "";
    errorDescripcion.textContent = "";
    errorCategoria.textContent = "";

}, 1000);

});

// ===============================
// CARGA INICIAL
// ===============================

renderizarCultivos();
