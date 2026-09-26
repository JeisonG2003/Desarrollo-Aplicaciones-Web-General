from flask import Flask, render_template, redirect, url_for, flash, request
from dotenv import load_dotenv
import os
import json

from psycopg2.extras import RealDictCursor

from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import get_db_connection
from models import Usuario

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm

# Cargar las variables del archivo .env al inicio
load_dotenv()

app = Flask(__name__)

# Clave secreta para Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."

# Configuración de la base de datos PostgreSQL
app.config["POSTGRES_HOST"] = os.getenv("POSTGRES_HOST")
app.config["POSTGRES_PORT"] = os.getenv("POSTGRES_PORT", "5432")
app.config["POSTGRES_DB"] = os.getenv("POSTGRES_DB")
app.config["POSTGRES_USER"] = os.getenv("POSTGRES_USER")
app.config["POSTGRES_PASSWORD"] = os.getenv("POSTGRES_PASSWORD")

# Cargar usuario desde PostgreSQL
@login_manager.user_loader
def load_user(user_id):

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return Usuario(
            usuario["id"],
            usuario["usuario"],
            usuario["password"]
        )

    return None

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Comprobar si el usuario ya existe
        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conn.close()

            flash(
                "El nombre de usuario ya está registrado.",
                "danger"
            )

            return render_template(
                "registro.html",
                form=form
            )

        # Generar hash de la contraseña
        password_hash = generate_password_hash(
            form.password.data
        )

        # Registrar el usuario
        cursor.execute("""
            INSERT INTO usuarios
            (usuario, password)
            VALUES (%s, %s)
        """, (
            form.usuario.data,
            password_hash
        ))

        conn.commit()
        cursor.close()
        conn.close()

        flash(
            "Usuario registrado correctamente. Ahora puedes iniciar sesión.",
            "success"
        )

        return redirect(url_for("login"))
    
    return render_template("registro.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Buscar el usuario en PostgreSQL
        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (form.usuario.data,))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        # Comprobar usuario y contraseña
        if usuario and check_password_hash(
            usuario["password"],
            form.password.data
        ):

            usuario_obj = Usuario(
                usuario["id"],
                usuario["usuario"],
                usuario["password"]
            )

            login_user(usuario_obj)

            flash(
                "Inicio de sesión correcto.",
                "success"
            )

            return redirect(url_for("dashboard"))

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Has cerrado sesión correctamente.", "success")

    return redirect(url_for("login"))

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
@login_required
def productos():

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

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
@login_required
def nuevo_producto():

    form = ProductoForm()

    # 1. Obtener los proveedores desde PostgreSQL
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre ASC
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    # 2. Cargar las opciones en el SelectField del formulario
    form.id_proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in proveedores
    ]

    # 3. Guardar cuando el formulario es válido
    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos
            (nombre, categoria, precio, stock, id_proveedor)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data
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
@login_required
def editar_producto(id_producto):

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # 1. Buscar el producto a editar
    cursor.execute("""
        SELECT *
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    if producto is None:
        cursor.close()
        conn.close()
        flash("El producto no existe.", "danger")
        return redirect(url_for("productos"))

    form = ProductoForm()

    # 2. Obtener lista de proveedores para el select
    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre ASC
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    # 3. Asignar choices al SelectField
    form.id_proveedor.choices = [
        (proveedor["id_proveedor"], proveedor["nombre"])
        for proveedor in proveedores
    ]

    # 4. Si la petición es GET, cargar los datos actuales en el formulario
    if request.method == "GET":
        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]
        form.id_proveedor.data = producto["id_proveedor"]

    # 5. Guardar los cambios si la validación pasa
    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data,
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
@login_required
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
@login_required
def clientes():

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_cliente,
            nombre,
            actividad,
            ubicacion,
            cedula,
            telefono,
            correo
        FROM clientes
        ORDER BY id_cliente
    """)

    clientes = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "clientes.html",
        clientes=clientes
    )


# Formulario para registrar clientes
@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clientes
            (nombre, actividad, ubicacion, cedula, telefono, correo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.actividad.data,
            form.ubicacion.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            f"Cliente '{form.nombre.data}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )

# Editar cliente
@app.route("/clientes/editar/<int:id_cliente>", methods=["GET", "POST"])
@login_required
def editar_cliente(id_cliente):

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    if cliente is None:
        flash("El cliente no existe.", "danger")
        return redirect(url_for("clientes"))

    form = ClienteForm()

    if request.method == "GET":
        form.nombre.data = cliente.get("nombre") or ""
        form.actividad.data = cliente.get("actividad") or ""
        form.ubicacion.data = cliente.get("ubicacion") or ""
        form.cedula.data = cliente.get("cedula") or ""
        form.telefono.data = cliente.get("telefono") or ""
        form.correo.data = cliente.get("correo") or ""

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clientes
            SET nombre = %s,
                actividad = %s,
                ubicacion = %s,
                cedula = %s,
                telefono = %s,
                correo = %s
            WHERE id_cliente = %s
        """, (
            form.nombre.data,
            form.actividad.data,
            form.ubicacion.data,
            form.cedula.data,
            form.telefono.data,
            form.correo.data,
            id_cliente
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            f"Cliente '{form.nombre.data}' actualizado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )

# Eliminar cliente
@app.route("/clientes/eliminar/<int:id_cliente>", methods=["POST"])
@login_required
def eliminar_cliente(id_cliente):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM clientes
        WHERE id_cliente = %s
    """, (id_cliente,))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Cliente eliminado correctamente.",
        "success"
    )

    return redirect(url_for("clientes"))

# Módulo Proveedores
@app.route("/proveedores")
@login_required
def proveedores():

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            id_proveedor,
            nombre,
            descripcion,
            estado,
            telefono,
            correo
        FROM proveedores
        ORDER BY id_proveedor
    """)

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# Formulario para registrar proveedores
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO proveedores
            (nombre, descripcion, estado, telefono, correo)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.estado.data,
            form.telefono.data,
            form.correo.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            f"Proveedor '{form.nombre.data}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )

# Editar proveedor
@app.route("/proveedores/editar/<int:id_proveedor>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id_proveedor):

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT *
        FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    if proveedor is None:
        flash("El proveedor no existe.", "danger")
        return redirect(url_for("proveedores"))

    form = ProveedorForm()

    if request.method == "GET":
        form.nombre.data = proveedor.get("nombre") or ""
        form.descripcion.data = proveedor.get("descripcion") or ""
        form.estado.data = proveedor.get("estado") or ""
        form.telefono.data = proveedor.get("telefono") or ""
        form.correo.data = proveedor.get("correo") or ""

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE proveedores
            SET nombre = %s,
                descripcion = %s,
                estado = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
        """, (
            form.nombre.data,
            form.descripcion.data,
            form.estado.data,
            form.telefono.data,
            form.correo.data,
            id_proveedor
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            f"Proveedor '{form.nombre.data}' actualizado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )

# Eliminar proveedor
@app.route("/proveedores/eliminar/<int:id_proveedor>", methods=["POST"])
@login_required
def eliminar_proveedor(id_proveedor):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM proveedores
        WHERE id_proveedor = %s
    """, (id_proveedor,))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(url_for("proveedores"))

# Módulo Facturación
@app.route("/facturacion")
@login_required
def facturacion():

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT
            f.id_factura,
            f.numero,
            f.fecha,
            f.total,
            c.nombre AS cliente,
            p.nombre AS producto
        FROM facturas f
        LEFT JOIN clientes c
            ON f.id_cliente = c.id_cliente
        LEFT JOIN productos p
            ON f.id_producto = p.id_producto
        ORDER BY f.id_factura
    """)

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        facturas=facturas
    )


# Formulario para registrar facturas
@app.route("/facturacion/nuevo", methods=["GET", "POST"])
@login_required
def nueva_factura():

    form = FacturacionForm()

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Obtener clientes desde PostgreSQL
    cursor.execute("""
        SELECT id_cliente, nombre
        FROM clientes
        ORDER BY nombre ASC
    """)

    clientes = cursor.fetchall()

    # Obtener productos con su precio desde PostgreSQL
    cursor.execute("""
        SELECT id_producto, nombre, precio
        FROM productos
        ORDER BY nombre ASC
    """)

    productos = cursor.fetchall()

    # Autogenerar el número de factura correlativo
    cursor.execute("SELECT COUNT(*) AS total_facturas FROM facturas")
    conteo = cursor.fetchone()["total_facturas"]
    numero_siguiente = f"FACT-{(conteo + 1):04d}"

    cursor.close()
    conn.close()

    # Cargar clientes en el SelectField
    form.id_cliente.choices = [
        (cliente["id_cliente"], cliente["nombre"])
        for cliente in clientes
    ]

    # Cargar productos en el SelectField (mostrando el precio)
    form.id_producto.choices = [
        (producto["id_producto"], f"{producto['nombre']} (${producto['precio']:.2f})")
        for producto in productos
    ]

    # Diccionario de precios para el cálculo automático con JavaScript
    precios_dict = {p["id_producto"]: float(p["precio"]) for p in productos}

    # Asignar número automático al cargar la página
    if request.method == "GET" and not form.numero.data:
        form.numero.data = numero_siguiente

    # Registrar factura
    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO facturas
            (numero, id_cliente, id_producto, total)
            VALUES (%s, %s, %s, %s)
        """, (
            form.numero.data,
            form.id_cliente.data,
            form.id_producto.data,
            form.total.data
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            f"Factura '{form.numero.data}' registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form,
        precios_json=json.dumps(precios_dict)
    )


# Editar factura
@app.route("/facturacion/editar/<int:id_factura>", methods=["GET", "POST"])
@login_required
def editar_factura(id_factura):

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # 1. Buscar la factura
    cursor.execute("""
        SELECT *
        FROM facturas
        WHERE id_factura = %s
    """, (id_factura,))

    factura = cursor.fetchone()

    if factura is None:
        cursor.close()
        conn.close()

        flash("La factura no existe.", "danger")

        return redirect(url_for("facturacion"))

    # 2. Obtener clientes
    cursor.execute("""
        SELECT id_cliente, nombre
        FROM clientes
        ORDER BY nombre ASC
    """)

    clientes = cursor.fetchall()

    # 3. Obtener productos con precio
    cursor.execute("""
        SELECT id_producto, nombre, precio
        FROM productos
        ORDER BY nombre ASC
    """)

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    form = FacturacionForm()

    # 4. Cargar opciones en los SelectField
    form.id_cliente.choices = [
        (cliente["id_cliente"], cliente["nombre"])
        for cliente in clientes
    ]

    form.id_producto.choices = [
        (producto["id_producto"], f"{producto['nombre']} (${producto['precio']:.2f})")
        for producto in productos
    ]

    precios_dict = {p["id_producto"]: float(p["precio"]) for p in productos}

    # 5. Cargar datos actuales cuando se abre el formulario
    if request.method == "GET":

        form.numero.data = factura["numero"]
        form.id_cliente.data = factura["id_cliente"]
        form.id_producto.data = factura["id_producto"]
        form.total.data = factura["total"]

    # 6. Guardar cambios
    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE facturas
            SET numero = %s,
                id_cliente = %s,
                id_producto = %s,
                total = %s
            WHERE id_factura = %s
        """, (
            form.numero.data,
            form.id_cliente.data,
            form.id_producto.data,
            form.total.data,
            id_factura
        ))

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            f"Factura '{form.numero.data}' actualizada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form,
        precios_json=json.dumps(precios_dict)
    )


# Eliminar factura
@app.route("/facturacion/eliminar/<int:id_factura>", methods=["POST"])
@login_required
def eliminar_factura(id_factura):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM facturas
        WHERE id_factura = %s
    """, (id_factura,))

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Factura eliminada correctamente.",
        "success"
    )

    return redirect(url_for("facturacion"))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)