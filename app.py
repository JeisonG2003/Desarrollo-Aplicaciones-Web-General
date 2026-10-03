from flask import Flask, render_template, redirect, url_for, flash, request, make_response
from dotenv import load_dotenv
import os
import json
from io import BytesIO
from decimal import Decimal, ROUND_HALF_UP
from functools import wraps

from xhtml2pdf import pisa
from psycopg.rows import dict_row

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from conexion.conexion import get_db_connection
from models import Usuario

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm, AnularFacturaForm
from forms.inventario_form import MovimientoInventarioForm
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

# Datos del emisor para la representación impresa académica tipo RIDE.
# Este proyecto NO se conecta al SRI ni genera autorizaciones tributarias reales.
app.config["EMISOR_RAZON_SOCIAL"] = os.getenv(
    "EMISOR_RAZON_SOCIAL",
    "AgroTech - Proyecto Académico"
)
app.config["EMISOR_NOMBRE_COMERCIAL"] = os.getenv(
    "EMISOR_NOMBRE_COMERCIAL",
    "AgroTech"
)
app.config["EMISOR_RUC"] = os.getenv(
    "EMISOR_RUC",
    "NO CONFIGURADO"
)
app.config["EMISOR_DIRECCION_MATRIZ"] = os.getenv(
    "EMISOR_DIRECCION_MATRIZ",
    "Dirección matriz no configurada"
)
app.config["EMISOR_DIRECCION_ESTABLECIMIENTO"] = os.getenv(
    "EMISOR_DIRECCION_ESTABLECIMIENTO",
    "Dirección establecimiento no configurada"
)
app.config["EMISOR_OBLIGADO_CONTABILIDAD"] = os.getenv(
    "EMISOR_OBLIGADO_CONTABILIDAD",
    "NO"
)
app.config["ESTABLECIMIENTO"] = os.getenv(
    "ESTABLECIMIENTO",
    "001"
)
app.config["PUNTO_EMISION"] = os.getenv(
    "PUNTO_EMISION",
    "001"
)


# Cargar usuario desde PostgreSQL
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, usuario, password, rol, estado
        FROM usuarios
        WHERE id = %s
        """,
        (user_id,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if usuario:
        return Usuario(
            usuario["id"],
            usuario["usuario"],
            usuario["password"],
            usuario.get("rol", "USUARIO"),
            usuario.get("estado", "ACTIVO")
        )

    return None


def admin_required(view_function):
    """Protege rutas que solo puede utilizar un ADMIN."""

    @wraps(view_function)
    @login_required
    def wrapped(*args, **kwargs):
        if getattr(current_user, "rol", "USUARIO") != "ADMIN":
            flash(
                "No tienes permisos de administrador para realizar esta acción.",
                "warning"
            )
            return redirect(url_for("dashboard"))

        return view_function(*args, **kwargs)

    return wrapped


def dinero(valor):
    return Decimal(str(valor or 0)).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )


@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = UsuarioForm()

    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT id FROM usuarios WHERE usuario = %s",
                (form.usuario.data,)
            )

            if cursor.fetchone():
                flash(
                    "El nombre de usuario ya está registrado.",
                    "danger"
                )
                return render_template(
                    "registro.html",
                    form=form
                )

            cursor.execute(
                "SELECT COUNT(*) AS total FROM usuarios"
            )

            es_primero = cursor.fetchone()["total"] == 0
            rol = "ADMIN" if es_primero else "USUARIO"
            password_hash = generate_password_hash(form.password.data)

            cursor.execute(
                """
                INSERT INTO usuarios (usuario, password, rol, estado)
                VALUES (%s, %s, %s, 'ACTIVO')
                """,
                (
                    form.usuario.data,
                    password_hash,
                    rol
                )
            )

            conn.commit()

            mensaje = "Usuario registrado correctamente."

            if es_primero:
                mensaje += (
                    " Al ser la primera cuenta, se asignó el rol ADMIN."
                )

            flash(
                mensaje + " Ahora puedes iniciar sesión.",
                "success"
            )

            return redirect(url_for("login"))

        finally:
            cursor.close()
            conn.close()

    return render_template(
        "registro.html",
        form=form
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, usuario, password, rol, estado
            FROM usuarios
            WHERE usuario = %s
            """,
            (form.usuario.data,)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario and usuario.get("estado") != "ACTIVO":
            flash(
                "Esta cuenta se encuentra inactiva. Contacta al administrador.",
                "warning"
            )

        elif usuario and check_password_hash(
            usuario["password"],
            form.password.data
        ):
            usuario_obj = Usuario(
                usuario["id"],
                usuario["usuario"],
                usuario["password"],
                usuario.get("rol", "USUARIO"),
                usuario.get("estado", "ACTIVO")
            )

            login_user(usuario_obj)

            flash(
                f"Bienvenido, {usuario['usuario']}. "
                f"Rol: {usuario.get('rol', 'USUARIO')}.",
                "success"
            )

            return redirect(url_for("dashboard"))

        else:
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

    flash(
        "Has cerrado sesión correctamente.",
        "success"
    )

    return redirect(url_for("login"))


# Página principal
@app.route("/")
def inicio():

    proyecto = {
        "nombre": "AgroTech",
        "descripcion": (
            "Plataforma digital para la gestión y control de "
            "actividades agrícolas"
        ),
        "materia": "Proyecto Integrador - Desarrollo de Aplicaciones Web",
        "autor": (
            "Cornejo Olaya Lissi Antonella y "
            "Jeison Teobaldo García Arreaga"
        )
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
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            p.id_producto,
            p.nombre,
            p.categoria,
            p.precio,
            p.stock,
            p.stock_minimo,
            p.iva_porcentaje,
            p.activo,
            p.id_proveedor,
            pr.nombre AS proveedor
        FROM productos p
        LEFT JOIN proveedores pr
            ON p.id_proveedor = pr.id_proveedor
        WHERE p.activo = TRUE OR %s = 'ADMIN'
        ORDER BY p.id_producto
        """,
        (getattr(current_user, "rol", "USUARIO"),)
    )

    productos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# Formulario para registrar productos
@app.route("/productos/nuevo", methods=["GET", "POST"])
@admin_required
def nuevo_producto():

    form = ProductoForm()

    # 1. Obtener los proveedores desde PostgreSQL
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre ASC
        """
    )

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

        cursor.execute(
            """
            INSERT INTO productos
            (nombre, categoria, precio, iva_porcentaje, stock, id_proveedor, activo)
            VALUES (%s, %s, %s, %s, %s, %s, TRUE)
            RETURNING id_producto
            """,
            (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.iva_porcentaje.data,
                form.stock.data,
                form.id_proveedor.data
            )
        )

        id_producto_nuevo = cursor.fetchone()["id_producto"]

        if form.stock.data > 0:
            cursor.execute(
                """
                INSERT INTO movimientos_inventario
                    (
                        id_producto,
                        tipo,
                        cantidad,
                        stock_anterior,
                        stock_nuevo,
                        id_usuario,
                        motivo
                    )
                VALUES (%s, 'ENTRADA', %s, 0, %s, %s, %s)
                """,
                (
                    id_producto_nuevo,
                    form.stock.data,
                    form.stock.data,
                    current_user.id,
                    "Stock inicial al registrar el producto"
                )
            )

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
@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@admin_required
def editar_producto(id_producto):

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Buscar el producto a editar
    cursor.execute(
        """
        SELECT *
        FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    producto = cursor.fetchone()

    if producto is None:
        cursor.close()
        conn.close()

        flash(
            "El producto no existe.",
            "danger"
        )

        return redirect(url_for("productos"))

    form = ProductoForm()

    # 2. Obtener lista de proveedores para el select
    cursor.execute(
        """
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre ASC
        """
    )

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
        form.iva_porcentaje.data = int(
            producto.get("iva_porcentaje") or 0
        )
        form.stock.data = producto["stock"]
        form.id_proveedor.data = producto["id_proveedor"]

    # 5. Guardar los cambios si la validación pasa
    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        stock_anterior = int(producto["stock"])
        stock_nuevo = int(form.stock.data)

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s,
                categoria = %s,
                precio = %s,
                iva_porcentaje = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
            """,
            (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.iva_porcentaje.data,
                stock_nuevo,
                form.id_proveedor.data,
                id_producto
            )
        )

        diferencia = stock_nuevo - stock_anterior

        if diferencia != 0:
            tipo = (
                'AJUSTE_ENTRADA'
                if diferencia > 0
                else 'AJUSTE_SALIDA'
            )

            cursor.execute(
                """
                INSERT INTO movimientos_inventario
                    (
                        id_producto,
                        tipo,
                        cantidad,
                        stock_anterior,
                        stock_nuevo,
                        id_usuario,
                        motivo
                    )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    id_producto,
                    tipo,
                    abs(diferencia),
                    stock_anterior,
                    stock_nuevo,
                    current_user.id,
                    "Ajuste realizado desde edición de producto"
                )
            )

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
@app.route(
    "/productos/eliminar/<int:id_producto>",
    methods=["POST"]
)
@admin_required
def eliminar_producto(id_producto):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nombre, activo FROM productos WHERE id_producto = %s",
        (id_producto,)
    )

    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()

        flash(
            "El producto no existe.",
            "danger"
        )

        return redirect(url_for("productos"))

    nuevo_estado = not bool(producto["activo"])

    cursor.execute(
        "UPDATE productos SET activo = %s WHERE id_producto = %s",
        (nuevo_estado, id_producto)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        f"Producto '{producto['nombre']}' "
        f"{'activado' if nuevo_estado else 'desactivado'} correctamente. "
        f"El historial se conserva.",
        "success"
    )

    return redirect(url_for("productos"))


# Módulo Clientes
@app.route("/clientes")
@login_required
def clientes():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
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
        """
    )

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

        cursor.execute(
            """
            INSERT INTO clientes
            (nombre, actividad, ubicacion, cedula, telefono, correo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.actividad.data,
                form.ubicacion.data,
                form.cedula.data,
                form.telefono.data,
                form.correo.data
            )
        )

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
@app.route(
    "/clientes/editar/<int:id_cliente>",
    methods=["GET", "POST"]
)
@login_required
def editar_cliente(id_cliente):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM clientes
        WHERE id_cliente = %s
        """,
        (id_cliente,)
    )

    cliente = cursor.fetchone()

    cursor.close()
    conn.close()

    if cliente is None:
        flash(
            "El cliente no existe.",
            "danger"
        )

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

        cursor.execute(
            """
            UPDATE clientes
            SET nombre = %s,
                actividad = %s,
                ubicacion = %s,
                cedula = %s,
                telefono = %s,
                correo = %s
            WHERE id_cliente = %s
            """,
            (
                form.nombre.data,
                form.actividad.data,
                form.ubicacion.data,
                form.cedula.data,
                form.telefono.data,
                form.correo.data,
                id_cliente
            )
        )

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
@app.route(
    "/clientes/eliminar/<int:id_cliente>",
    methods=["POST"]
)
@login_required
def eliminar_cliente(id_cliente):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM clientes
        WHERE id_cliente = %s
        """,
        (id_cliente,)
    )

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
@admin_required
def proveedores():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id_proveedor,
            nombre,
            descripcion,
            estado,
            telefono,
            correo
        FROM proveedores
        ORDER BY id_proveedor
        """
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "proveedores.html",
        proveedores=proveedores
    )


# Formulario para registrar proveedores
@app.route("/proveedores/nuevo", methods=["GET", "POST"])
@admin_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO proveedores
            (nombre, descripcion, estado, telefono, correo)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.estado.data,
                form.telefono.data,
                form.correo.data
            )
        )

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
@app.route(
    "/proveedores/editar/<int:id_proveedor>",
    methods=["GET", "POST"]
)
@admin_required
def editar_proveedor(id_proveedor):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM proveedores
        WHERE id_proveedor = %s
        """,
        (id_proveedor,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    if proveedor is None:
        flash(
            "El proveedor no existe.",
            "danger"
        )

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

        cursor.execute(
            """
            UPDATE proveedores
            SET nombre = %s,
                descripcion = %s,
                estado = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
            """,
            (
                form.nombre.data,
                form.descripcion.data,
                form.estado.data,
                form.telefono.data,
                form.correo.data,
                id_proveedor
            )
        )

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
@app.route(
    "/proveedores/eliminar/<int:id_proveedor>",
    methods=["POST"]
)
@admin_required
def eliminar_proveedor(id_proveedor):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM proveedores
        WHERE id_proveedor = %s
        """,
        (id_proveedor,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Proveedor eliminado correctamente.",
        "success"
    )

    return redirect(url_for("proveedores"))


# ============================================================
# Módulo Facturación / Inventario / Administración
# ============================================================


def obtener_catalogos_factura(cursor):
    cursor.execute(
        """
        SELECT id_cliente, nombre, cedula, ubicacion, telefono, correo
        FROM clientes
        ORDER BY nombre ASC
        """
    )

    clientes = cursor.fetchall()

    cursor.execute(
        """
        SELECT id_producto, nombre, precio, stock, iva_porcentaje
        FROM productos
        WHERE activo = TRUE
        ORDER BY nombre ASC
        """
    )

    productos = cursor.fetchall()

    return clientes, productos


@app.route("/facturacion")
@login_required
def facturacion():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            f.id_factura,
            f.numero,
            f.fecha,
            f.total,
            f.estado,
            c.nombre AS cliente,
            COALESCE(SUM(d.cantidad), 0) AS unidades,
            COUNT(d.id_detalle) AS lineas,
            COALESCE(
                STRING_AGG(
                    p.nombre || ' x' || d.cantidad::text,
                    ', ' ORDER BY d.id_detalle
                ),
                ''
            ) AS productos
        FROM facturas f
        LEFT JOIN clientes c
            ON f.id_cliente = c.id_cliente
        LEFT JOIN detalle_factura d
            ON f.id_factura = d.id_factura
        LEFT JOIN productos p
            ON d.id_producto = p.id_producto
        GROUP BY f.id_factura, c.nombre
        ORDER BY f.id_factura DESC
        """
    )

    facturas = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "facturacion.html",
        facturas=facturas,
        anular_form=AnularFacturaForm()
    )


@app.route("/facturacion/<int:id_factura>/pdf")
@login_required
def factura_pdf(id_factura):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            f.*,
            c.nombre AS cliente,
            c.cedula,
            c.ubicacion,
            c.telefono,
            c.correo,
            u.usuario AS usuario_emisor
        FROM facturas f
        LEFT JOIN clientes c
            ON f.id_cliente = c.id_cliente
        LEFT JOIN usuarios u
            ON f.id_usuario = u.id
        WHERE f.id_factura = %s
        """,
        (id_factura,)
    )

    factura = cursor.fetchone()

    if factura:
        cursor.execute(
            """
            SELECT
                d.id_detalle,
                d.id_producto,
                p.nombre AS producto,
                d.cantidad,
                d.precio_unitario,
                d.iva_porcentaje,
                d.base_imponible,
                d.valor_iva,
                d.subtotal,
                p.categoria
            FROM detalle_factura d
            JOIN productos p
                ON p.id_producto = d.id_producto
            WHERE d.id_factura = %s
            ORDER BY d.id_detalle
            """,
            (id_factura,)
        )

        detalles = cursor.fetchall()

    else:
        detalles = []

    cursor.close()
    conn.close()

    if factura is None:
        flash(
            "La factura no existe.",
            "danger"
        )

        return redirect(url_for("facturacion"))

    logo_path = os.path.join(
        app.root_path,
        "static",
        "img",
        "logo-agrotech.png"
    )

    emisor = {
        "razon_social": app.config["EMISOR_RAZON_SOCIAL"],
        "nombre_comercial": app.config["EMISOR_NOMBRE_COMERCIAL"],
        "ruc": app.config["EMISOR_RUC"],
        "direccion_matriz": app.config["EMISOR_DIRECCION_MATRIZ"],
        "direccion_establecimiento": app.config[
            "EMISOR_DIRECCION_ESTABLECIMIENTO"
        ],
        "obligado_contabilidad": app.config[
            "EMISOR_OBLIGADO_CONTABILIDAD"
        ],
    }

    html = render_template(
        "factura_pdf.html",
        factura=factura,
        detalles=detalles,
        logo_path=logo_path,
        emisor=emisor
    )

    pdf_buffer = BytesIO()

    resultado = pisa.CreatePDF(
        BytesIO(html.encode("UTF-8")),
        dest=pdf_buffer
    )

    if resultado.err:
        return "Error al generar el PDF de la factura.", 500

    response = make_response(
        pdf_buffer.getvalue()
    )

    pdf_buffer.close()

    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = (
        f'inline; filename="Factura_{factura["numero"]}.pdf"'
    )

    return response


@app.route("/facturacion/nuevo", methods=["GET", "POST"])
@login_required
def nueva_factura():

    form = FacturacionForm()

    conn = get_db_connection()
    cursor = conn.cursor()

    clientes, productos = obtener_catalogos_factura(cursor)

    form.id_cliente.choices = [
        (c["id_cliente"], c["nombre"])
        for c in clientes
    ]

    productos_front = [
        {
            "id": p["id_producto"],
            "nombre": p["nombre"],
            "precio": float(p["precio"]),
            "stock": int(p["stock"]),
            "iva": float(p.get("iva_porcentaje") or 0)
        }
        for p in productos
    ]

    # Datos del cliente para mostrarlos automáticamente al seleccionarlo.
    # No se vuelven a escribir en el formulario: se toman de la tabla clientes.
    clientes_front = [
        {
            "id": c["id_cliente"],
            "nombre": c["nombre"] or "",
            "cedula": c["cedula"] or "",
            "ubicacion": c["ubicacion"] or "",
            "telefono": c["telefono"] or "",
            "correo": c["correo"] or ""
        }
        for c in clientes
    ]

    if request.method == "GET":
        form.numero.data = "001-001-(se asigna al guardar)"

    if form.validate_on_submit():

        try:
            detalle_recibido = json.loads(
                form.detalle_json.data
            )

            if (
                not isinstance(detalle_recibido, list)
                or not detalle_recibido
            ):
                raise ValueError("Detalle vacío")

            # Consolidar por producto para evitar duplicados manipulados en el navegador.
            cantidades = {}

            for item in detalle_recibido:
                pid = int(item.get("id_producto"))
                cantidad = int(item.get("cantidad"))

                if cantidad <= 0:
                    raise ValueError("Cantidad inválida")

                cantidades[pid] = (
                    cantidades.get(pid, 0) + cantidad
                )

            ids = list(cantidades.keys())

            cursor.execute(
                """
                SELECT id_producto, nombre, precio, stock, iva_porcentaje, activo
                FROM productos
                WHERE id_producto = ANY(%s)
                FOR UPDATE
                """,
                (ids,)
            )

            productos_bd = {
                p["id_producto"]: p
                for p in cursor.fetchall()
            }

            if len(productos_bd) != len(ids):
                raise ValueError(
                    "Uno de los productos ya no existe."
                )

            detalles_calculados = []

            subtotal_0 = Decimal("0.00")
            subtotal_15 = Decimal("0.00")
            iva_15 = Decimal("0.00")

            for pid, cantidad in cantidades.items():

                producto = productos_bd[pid]

                if not producto.get("activo", True):
                    raise ValueError(
                        f"El producto {producto['nombre']} está inactivo."
                    )

                stock = int(producto["stock"])

                if cantidad > stock:
                    raise ValueError(
                        f"Stock insuficiente para {producto['nombre']}. "
                        f"Disponible: {stock}; solicitado: {cantidad}."
                    )

                precio = dinero(producto["precio"])

                iva_pct = Decimal(
                    str(producto.get("iva_porcentaje") or 0)
                )

                base = dinero(
                    precio * cantidad
                )

                valor_iva = dinero(
                    base * iva_pct / Decimal("100")
                )

                subtotal_linea = dinero(
                    base + valor_iva
                )

                if iva_pct == Decimal("15"):
                    subtotal_15 += base
                    iva_15 += valor_iva
                else:
                    subtotal_0 += base

                detalles_calculados.append(
                    {
                        "id_producto": pid,
                        "cantidad": cantidad,
                        "precio": precio,
                        "iva_pct": iva_pct,
                        "base": base,
                        "valor_iva": valor_iva,
                        "subtotal": subtotal_linea,
                        "stock_anterior": stock,
                        "stock_nuevo": stock - cantidad,
                        "nombre": producto["nombre"],
                    }
                )

            subtotal_0 = dinero(subtotal_0)
            subtotal_15 = dinero(subtotal_15)
            iva_15 = dinero(iva_15)

            subtotal_sin_impuestos = dinero(
                subtotal_0 + subtotal_15
            )

            total = dinero(
                subtotal_sin_impuestos + iva_15
            )

            cursor.execute(
                "SELECT nextval('factura_secuencial_seq') AS secuencial"
            )

            secuencial = int(
                cursor.fetchone()["secuencial"]
            )

            numero = (
                f"{app.config['ESTABLECIMIENTO']}-"
                f"{app.config['PUNTO_EMISION']}-"
                f"{secuencial:09d}"
            )

            cursor.execute(
                """
                INSERT INTO facturas (
                    numero,
                    id_cliente,
                    fecha,
                    total,
                    id_usuario,
                    estado,
                    forma_pago,
                    observaciones,
                    subtotal_sin_impuestos,
                    base_iva_0,
                    base_iva_15,
                    iva_15,
                    total_descuento
                )
                VALUES (
                    %s,
                    %s,
                    CURRENT_DATE,
                    %s,
                    %s,
                    'ACTIVA',
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    0
                )
                RETURNING id_factura
                """,
                (
                    numero,
                    form.id_cliente.data,
                    total,
                    current_user.id,
                    form.forma_pago.data,
                    form.observaciones.data,
                    subtotal_sin_impuestos,
                    subtotal_0,
                    subtotal_15,
                    iva_15
                )
            )

            id_factura = cursor.fetchone()["id_factura"]

            for d in detalles_calculados:

                cursor.execute(
                    """
                    INSERT INTO detalle_factura (
                        id_factura,
                        id_producto,
                        cantidad,
                        precio_unitario,
                        iva_porcentaje,
                        base_imponible,
                        valor_iva,
                        subtotal
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        id_factura,
                        d["id_producto"],
                        d["cantidad"],
                        d["precio"],
                        d["iva_pct"],
                        d["base"],
                        d["valor_iva"],
                        d["subtotal"]
                    )
                )

                cursor.execute(
                    """
                    UPDATE productos
                    SET stock = %s
                    WHERE id_producto = %s
                    """,
                    (
                        d["stock_nuevo"],
                        d["id_producto"]
                    )
                )

                cursor.execute(
                    """
                    INSERT INTO movimientos_inventario (
                        id_producto,
                        tipo,
                        cantidad,
                        stock_anterior,
                        stock_nuevo,
                        id_factura,
                        id_usuario,
                        motivo
                    )
                    VALUES (%s, 'SALIDA_VENTA', %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        d["id_producto"],
                        d["cantidad"],
                        d["stock_anterior"],
                        d["stock_nuevo"],
                        id_factura,
                        current_user.id,
                        f"Venta registrada en factura {numero}"
                    )
                )

            conn.commit()

            flash(
                f"Factura {numero} registrada. "
                f"El inventario fue actualizado automáticamente.",
                "success"
            )

            return redirect(
                url_for(
                    "factura_pdf",
                    id_factura=id_factura
                )
            )

        except (
            ValueError,
            TypeError,
            json.JSONDecodeError
        ) as exc:

            conn.rollback()

            flash(
                str(exc),
                "danger"
            )

        except Exception:

            conn.rollback()

            app.logger.exception(
                "Error registrando factura"
            )

            flash(
                "No fue posible registrar la factura. "
                "No se realizó ningún cambio en el inventario.",
                "danger"
            )

    cursor.close()
    conn.close()

    return render_template(
        "formulario_facturacion.html",
        form=form,
        productos_json=json.dumps(
            productos_front,
            ensure_ascii=False
        ),
        clientes_json=json.dumps(
            clientes_front,
            ensure_ascii=False
        )
    )


@app.route(
    "/facturacion/anular/<int:id_factura>",
    methods=["POST"]
)
@admin_required
def anular_factura(id_factura):

    form = AnularFacturaForm()

    if not form.validate_on_submit():
        flash(
            "Indique un motivo válido para anular la factura.",
            "danger"
        )

        return redirect(url_for("facturacion"))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT *
            FROM facturas
            WHERE id_factura = %s
            FOR UPDATE
            """,
            (id_factura,)
        )

        factura = cursor.fetchone()

        if not factura:
            flash(
                "La factura no existe.",
                "danger"
            )

            return redirect(url_for("facturacion"))

        if factura["estado"] == "ANULADA":
            flash(
                "La factura ya se encuentra anulada.",
                "warning"
            )

            return redirect(url_for("facturacion"))

        cursor.execute(
            """
            SELECT id_producto, cantidad
            FROM detalle_factura
            WHERE id_factura = %s
            ORDER BY id_detalle
            """,
            (id_factura,)
        )

        detalles = cursor.fetchall()

        for d in detalles:

            cursor.execute(
                """
                SELECT stock
                FROM productos
                WHERE id_producto = %s
                FOR UPDATE
                """,
                (d["id_producto"],)
            )

            stock_anterior = int(
                cursor.fetchone()["stock"]
            )

            stock_nuevo = (
                stock_anterior + int(d["cantidad"])
            )

            cursor.execute(
                """
                UPDATE productos
                SET stock = %s
                WHERE id_producto = %s
                """,
                (
                    stock_nuevo,
                    d["id_producto"]
                )
            )

            cursor.execute(
                """
                INSERT INTO movimientos_inventario (
                    id_producto,
                    tipo,
                    cantidad,
                    stock_anterior,
                    stock_nuevo,
                    id_factura,
                    id_usuario,
                    motivo
                )
                VALUES (%s, 'REVERSO_VENTA', %s, %s, %s, %s, %s, %s)
                """,
                (
                    d["id_producto"],
                    d["cantidad"],
                    stock_anterior,
                    stock_nuevo,
                    id_factura,
                    current_user.id,
                    f"Anulación de {factura['numero']}: "
                    f"{form.motivo.data}"
                )
            )

        cursor.execute(
            """
            UPDATE facturas
            SET estado = 'ANULADA',
                motivo_anulacion = %s,
                fecha_anulacion = CURRENT_TIMESTAMP
            WHERE id_factura = %s
            """,
            (
                form.motivo.data,
                id_factura
            )
        )

        conn.commit()

        flash(
            f"Factura {factura['numero']} anulada. "
            f"El stock fue devuelto al inventario.",
            "success"
        )

    except Exception:

        conn.rollback()

        app.logger.exception(
            "Error anulando factura"
        )

        flash(
            "No se pudo anular la factura. "
            "No se aplicaron cambios parciales.",
            "danger"
        )

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("facturacion"))


@app.route("/inventario", methods=["GET", "POST"])
@admin_required
def inventario():

    form = MovimientoInventarioForm()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_producto, nombre, stock
        FROM productos
        WHERE activo = TRUE
        ORDER BY nombre
        """
    )

    catalogo = cursor.fetchall()

    form.id_producto.choices = [
        (
            p["id_producto"],
            f"{p['nombre']} (stock: {p['stock']})"
        )
        for p in catalogo
    ]

    if form.validate_on_submit():

        try:
            cursor.execute(
                """
                SELECT id_producto, nombre, stock
                FROM productos
                WHERE id_producto = %s
                FOR UPDATE
                """,
                (form.id_producto.data,)
            )

            producto = cursor.fetchone()

            if not producto:
                raise ValueError(
                    "El producto seleccionado no existe."
                )

            stock_anterior = int(
                producto["stock"]
            )

            cantidad = int(
                form.cantidad.data
            )

            if form.tipo.data in (
                "ENTRADA",
                "AJUSTE_ENTRADA"
            ):
                stock_nuevo = (
                    stock_anterior + cantidad
                )

            else:
                if cantidad > stock_anterior:
                    raise ValueError(
                        f"Stock insuficiente. "
                        f"Disponible: {stock_anterior}."
                    )

                stock_nuevo = (
                    stock_anterior - cantidad
                )

            cursor.execute(
                """
                UPDATE productos
                SET stock = %s
                WHERE id_producto = %s
                """,
                (
                    stock_nuevo,
                    producto["id_producto"]
                )
            )

            cursor.execute(
                """
                INSERT INTO movimientos_inventario (
                    id_producto,
                    tipo,
                    cantidad,
                    stock_anterior,
                    stock_nuevo,
                    id_usuario,
                    motivo
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    producto["id_producto"],
                    form.tipo.data,
                    cantidad,
                    stock_anterior,
                    stock_nuevo,
                    current_user.id,
                    form.motivo.data
                )
            )

            conn.commit()

            flash(
                f"Movimiento registrado. "
                f"{producto['nombre']}: "
                f"{stock_anterior} → {stock_nuevo}.",
                "success"
            )

            return redirect(url_for("inventario"))

        except ValueError as exc:

            conn.rollback()

            flash(
                str(exc),
                "danger"
            )

        except Exception:

            conn.rollback()

            app.logger.exception(
                "Error en movimiento de inventario"
            )

            flash(
                "No se pudo registrar el movimiento.",
                "danger"
            )

    cursor.execute(
        """
        SELECT
            m.*,
            p.nombre AS producto,
            u.usuario,
            f.numero AS factura_numero
        FROM movimientos_inventario m
        JOIN productos p
            ON p.id_producto = m.id_producto
        LEFT JOIN usuarios u
            ON u.id = m.id_usuario
        LEFT JOIN facturas f
            ON f.id_factura = m.id_factura
        ORDER BY m.id_movimiento DESC
        LIMIT 200
        """
    )

    movimientos = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "inventario.html",
        form=form,
        movimientos=movimientos
    )


@app.route("/usuarios")
@admin_required
def usuarios_admin():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, usuario, rol, estado
        FROM usuarios
        ORDER BY id
        """
    )

    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    # FlaskForm base aporta token CSRF para acciones simples.
    from flask_wtf import FlaskForm

    return render_template(
        "usuarios_admin.html",
        usuarios=usuarios,
        accion_form=FlaskForm()
    )


@app.route(
    "/usuarios/<int:id_usuario>/rol",
    methods=["POST"]
)
@admin_required
def cambiar_rol_usuario(id_usuario):

    from flask_wtf import FlaskForm

    form = FlaskForm()

    if not form.validate_on_submit():
        flash(
            "Solicitud no válida.",
            "danger"
        )

        return redirect(
            url_for("usuarios_admin")
        )

    nuevo_rol = request.form.get(
        "rol",
        ""
    ).upper()

    if nuevo_rol not in (
        "ADMIN",
        "USUARIO"
    ):
        flash(
            "Rol no válido.",
            "danger"
        )

        return redirect(
            url_for("usuarios_admin")
        )

    if (
        id_usuario == int(current_user.id)
        and nuevo_rol != "ADMIN"
    ):
        flash(
            "No puedes quitarte tu propio rol de administrador.",
            "warning"
        )

        return redirect(
            url_for("usuarios_admin")
        )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET rol = %s
        WHERE id = %s
        """,
        (
            nuevo_rol,
            id_usuario
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Rol actualizado correctamente.",
        "success"
    )

    return redirect(
        url_for("usuarios_admin")
    )


@app.route(
    "/usuarios/<int:id_usuario>/estado",
    methods=["POST"]
)
@admin_required
def cambiar_estado_usuario(id_usuario):

    from flask_wtf import FlaskForm

    form = FlaskForm()

    if not form.validate_on_submit():
        flash(
            "Solicitud no válida.",
            "danger"
        )

        return redirect(
            url_for("usuarios_admin")
        )

    nuevo_estado = request.form.get(
        "estado",
        ""
    ).upper()

    if nuevo_estado not in (
        "ACTIVO",
        "INACTIVO"
    ):
        flash(
            "Estado no válido.",
            "danger"
        )

        return redirect(
            url_for("usuarios_admin")
        )

    if (
        id_usuario == int(current_user.id)
        and nuevo_estado != "ACTIVO"
    ):
        flash(
            "No puedes desactivar tu propia cuenta.",
            "warning"
        )

        return redirect(
            url_for("usuarios_admin")
        )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET estado = %s
        WHERE id = %s
        """,
        (
            nuevo_estado,
            id_usuario
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    flash(
        "Estado del usuario actualizado.",
        "success"
    )

    return redirect(
        url_for("usuarios_admin")
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)