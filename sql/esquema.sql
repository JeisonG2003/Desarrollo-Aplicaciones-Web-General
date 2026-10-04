-- ============================================================
-- AGROTECH - ESQUEMA POSTGRESQL
-- ============================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'USUARIO' CHECK (rol IN ('ADMIN','USUARIO')),
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO' CHECK (estado IN ('ACTIVO','INACTIVO'))
);

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(200), estado VARCHAR(20), telefono VARCHAR(20), correo VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    actividad VARCHAR(100), ubicacion VARCHAR(100), cedula VARCHAR(20), telefono VARCHAR(20), correo VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    iva_porcentaje DECIMAL(5,2) NOT NULL DEFAULT 15 CHECK (iva_porcentaje IN (0,15)),
    stock INT NOT NULL CHECK (stock >= 0),
    stock_minimo INT NOT NULL DEFAULT 5,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    id_proveedor INT REFERENCES proveedores(id_proveedor)
);

CREATE SEQUENCE IF NOT EXISTS factura_secuencial_seq START WITH 1;

CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    numero VARCHAR(20) UNIQUE NOT NULL,
    id_cliente INT REFERENCES clientes(id_cliente),
    id_usuario INT REFERENCES usuarios(id),
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVA' CHECK (estado IN ('ACTIVA','ANULADA')),
    forma_pago VARCHAR(10) NOT NULL DEFAULT '01',
    observaciones VARCHAR(300), motivo_anulacion VARCHAR(300), fecha_anulacion TIMESTAMP,
    subtotal_sin_impuestos DECIMAL(12,2) NOT NULL DEFAULT 0,
    base_iva_0 DECIMAL(12,2) NOT NULL DEFAULT 0,
    base_iva_15 DECIMAL(12,2) NOT NULL DEFAULT 0,
    iva_15 DECIMAL(12,2) NOT NULL DEFAULT 0,
    total_descuento DECIMAL(12,2) NOT NULL DEFAULT 0,
    total DECIMAL(12,2) NOT NULL CHECK (total >= 0)
);

CREATE TABLE IF NOT EXISTS detalle_factura (
    id_detalle SERIAL PRIMARY KEY,
    id_factura INT NOT NULL REFERENCES facturas(id_factura),
    id_producto INT NOT NULL REFERENCES productos(id_producto),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(12,2) NOT NULL CHECK (precio_unitario >= 0),
    iva_porcentaje DECIMAL(5,2) NOT NULL DEFAULT 0 CHECK (iva_porcentaje IN (0,15)),
    base_imponible DECIMAL(12,2) NOT NULL DEFAULT 0,
    valor_iva DECIMAL(12,2) NOT NULL DEFAULT 0,
    subtotal DECIMAL(12,2) NOT NULL CHECK (subtotal >= 0)
);

CREATE TABLE IF NOT EXISTS movimientos_inventario (
    id_movimiento SERIAL PRIMARY KEY,
    id_producto INT NOT NULL REFERENCES productos(id_producto),
    tipo VARCHAR(30) NOT NULL CHECK (tipo IN ('ENTRADA','SALIDA_VENTA','REVERSO_VENTA','AJUSTE_ENTRADA','AJUSTE_SALIDA')),
    cantidad INT NOT NULL CHECK (cantidad > 0),
    stock_anterior INT NOT NULL CHECK (stock_anterior >= 0),
    stock_nuevo INT NOT NULL CHECK (stock_nuevo >= 0),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_factura INT REFERENCES facturas(id_factura),
    id_usuario INT REFERENCES usuarios(id),
    motivo VARCHAR(300) NOT NULL
);
