const formulario = document.getElementById("formCultivo");
const listaCultivos = document.getElementById("listaCultivos");
const mensaje = document.getElementById("mensaje");
const totalRegistros = document.getElementById("totalRegistros");

let contador = 0;

formulario.addEventListener("submit", function(event) {

    event.preventDefault();

    const nombre = document.getElementById("nombre").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();
    const categoria = document.getElementById("categoria").value;

    if (nombre === "" || descripcion === "" || categoria === "") {

        mensaje.innerHTML = `
        <div class="alert alert-danger">
            Por favor complete todos los campos del formulario.
        </div>
        `;

        return;
    }


    const cultivo = document.createElement("div");

    cultivo.className = "card p-3 mb-3";


    cultivo.innerHTML = `
        <h5>${nombre}</h5>
        <p><strong>Categoría:</strong> ${categoria}</p>
        <p>${descripcion}</p>
    `;


    const botonEliminar = document.createElement("button");

    botonEliminar.textContent = "Eliminar registro";

    botonEliminar.className = "btn btn-danger";


    botonEliminar.addEventListener("click", function(){

        cultivo.remove();

        contador--;

        totalRegistros.textContent = contador;

        mensaje.innerHTML = `
        <div class="alert alert-warning">
            Registro eliminado correctamente.
        </div>
        `;

    });


    cultivo.appendChild(botonEliminar);


    listaCultivos.appendChild(cultivo);


    contador++;

    totalRegistros.textContent = contador;


    mensaje.innerHTML = `
    <div class="alert alert-success">
        Cultivo registrado correctamente.
    </div>
    `;


    formulario.reset();

});