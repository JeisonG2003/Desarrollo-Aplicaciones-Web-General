from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

app = Flask(__name__)

# Clave secreta para Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "agrotech-clave-secreta-2026"

# Página principal
@app.route("/")
def inicio():

    proyecto = {
        "nombre": "AgroTech",
        "descripcion": "Plataforma digital para la gestión y control de actividades agrícolas",
        "autor": "Jeison Teobaldo García Arreaga"
    }

    return render_template(
        "index.html",
        proyecto=proyecto
    )


# Módulo Productos
@app.route("/productos")
def productos():

    productos = [
        {
            "nombre": "Semillas de Maíz",
            "categoria": "Semillas",
            "precio": 12.50,
            "stock": 15
        },
        {
            "nombre": "Fertilizante Orgánico",
            "categoria": "Fertilizantes",
            "precio": 25.00,
            "stock": 8
        },
        {
            "nombre": "Herramientas Agrícolas",
            "categoria": "Herramientas",
            "precio": 35.00,
            "stock": 0
        }
    ]

    return render_template(
        "productos.html",
        productos=productos
    )


# Formulario para registrar productos
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        flash(
            f"Producto '{form.nombre.data}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )

# Módulo Clientes
@app.route("/clientes")
def clientes():

    clientes = [
        {
            "nombre": "Juan Pérez",
            "actividad": "Productor agrícola",
            "ubicacion": "Guayas"
        },
        {
            "nombre": "María González",
            "actividad": "Productora agrícola",
            "ubicacion": "Los Ríos"
        },
        {
            "nombre": "Carlos Rodríguez",
            "actividad": "Productor agrícola",
            "ubicacion": "Manabí"
        }
    ]

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# Formulario para registrar clientes
@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        flash(
            f"Cliente '{form.nombre.data}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )

# Módulo Proveedores
@app.route("/proveedores")
def proveedores():

    proveedores = [
        {
            "nombre": "Agroinsumos Ecuador",
            "descripcion": "Proveedor de semillas e insumos agrícolas.",
            "estado": "Activo"
        },
        {
            "nombre": "Campo Verde",
            "descripcion": "Proveedor de herramientas para actividades agrícolas.",
            "estado": "Activo"
        },
        {
            "nombre": "AgroSoluciones",
            "descripcion": "Proveedor de productos y recursos agrícolas.",
            "estado": "Inactivo"
        }
    ]

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )

# Formulario para registrar proveedores
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        flash(
            f"Proveedor '{form.nombre.data}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )

# Módulo Facturación
@app.route("/facturacion")
def facturacion():

    facturas = [
        {
            "numero": "001-001",
            "cliente": "Juan Pérez",
            "producto": "Maíz",
            "total": 120.00
        },
        {
            "numero": "001-002",
            "cliente": "María González",
            "producto": "Banano",
            "total": 180.00
        },
        {
            "numero": "001-003",
            "cliente": "Juan Pérez",
            "producto": "Tomate",
            "total": 95.00
        }
    ]

    return render_template(
        "facturacion.html",
        facturas=facturas
    )

# Formulario para registrar facturas
@app.route("/facturacion/nuevo", methods=["GET", "POST"])
def nueva_factura():

    form = FacturacionForm()

    if form.validate_on_submit():

        flash(
            f"Factura '{form.numero.data}' registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


if __name__ == "__main__":
    app.run(debug=True)