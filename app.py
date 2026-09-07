from flask import Flask, render_template, redirect, url_for, flash, request
from dotenv import load_dotenv
import os
from conexion.conexion import get_db_connection

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

# Cargar las variables del archivo .env al inicio
load_dotenv()

app = Flask(__name__)

# Clave secreta para Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "agrotech-clave-secreta-2026"

# Configuración de la base de datos MySQL
# Configuración de la base de datos MySQL
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DATABASE"] = os.getenv("MYSQL_DATABASE")
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

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT
        p.id_producto,
        p.nombre,
        p.categoria,
        p.precio,
        p.stock,
        p.id_proveedor,
        pr.nombre AS proveedor
    FROM productos p
    LEFT JOIN proveedores pr
        ON p.id_proveedor = pr.id_proveedor
""")

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# Formulario para registrar productos
@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, categoria, precio, stock)
            VALUES (%s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            f"Producto '{form.nombre.data}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )

# Editar producto
@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
def editar_producto(id_producto):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Buscar el producto seleccionado
    cursor.execute("""
        SELECT *
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    cursor.close()
    conn.close()

    if producto is None:
        flash("El producto no existe.", "danger")
        return redirect(url_for("productos"))

    form = ProductoForm()

    # Cargar los datos actuales cuando se abre el formulario
    if request.method == "GET":
        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

    # Guardar los cambios
    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            id_producto
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            f"Producto '{form.nombre.data}' actualizado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )

# Eliminar producto
@app.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
def eliminar_producto(id_producto):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Producto eliminado correctamente.",
        "success"
    )

    return redirect(url_for("productos"))

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