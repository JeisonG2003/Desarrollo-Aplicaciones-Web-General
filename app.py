from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)