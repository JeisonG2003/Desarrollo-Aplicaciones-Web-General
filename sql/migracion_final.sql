-- ============================================================
-- AGROTECH - MEJORAS DE ESQUEMA POSTGRESQL
-- ============================================================

BEGIN;

-- 1) ROLES Y ESTADO DE USUARIO
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS rol VARCHAR(20);
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS estado VARCHAR(20);
UPDATE usuarios SET rol = 'USUARIO' WHERE rol IS NULL OR rol NOT IN ('ADMIN','USUARIO');
UPDATE usuarios SET estado = 'ACTIVO' WHERE estado IS NULL OR estado NOT IN ('ACTIVO','INACTIVO');
ALTER TABLE usuarios ALTER COLUMN rol SET DEFAULT 'USUARIO';
ALTER TABLE usuarios ALTER COLUMN rol SET NOT NULL;
ALTER TABLE usuarios ALTER COLUMN estado SET DEFAULT 'ACTIVO';
ALTER TABLE usuarios ALTER COLUMN estado SET NOT NULL;
ALTER TABLE usuarios DROP CONSTRAINT IF EXISTS chk_usuario_rol;
ALTER TABLE usuarios ADD CONSTRAINT chk_usuario_rol CHECK (rol IN ('ADMIN','USUARIO'));
ALTER TABLE usuarios DROP CONSTRAINT IF EXISTS chk_usuario_estado;
ALTER TABLE usuarios ADD CONSTRAINT chk_usuario_estado CHECK (estado IN ('ACTIVO','INACTIVO'));

UPDATE usuarios SET rol = 'ADMIN'
WHERE id = (SELECT MIN(id) FROM usuarios)
  AND NOT EXISTS (SELECT 1 FROM usuarios WHERE rol = 'ADMIN');

-- 2) PRODUCTOS / INVENTARIO
ALTER TABLE productos ADD COLUMN IF NOT EXISTS iva_porcentaje DECIMAL(5,2);
UPDATE productos SET iva_porcentaje = 0 WHERE iva_porcentaje IS NULL;
ALTER TABLE productos ALTER COLUMN iva_porcentaje SET DEFAULT 15.00;
ALTER TABLE productos ALTER COLUMN iva_porcentaje SET NOT NULL;
ALTER TABLE productos ADD COLUMN IF NOT EXISTS stock_minimo INT NOT NULL DEFAULT 5;
ALTER TABLE productos ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE;
ALTER TABLE productos DROP CONSTRAINT IF EXISTS chk_producto_stock;
ALTER TABLE productos ADD CONSTRAINT chk_producto_stock CHECK (stock >= 0);
ALTER TABLE productos DROP CONSTRAINT IF EXISTS chk_producto_iva;
ALTER TABLE productos ADD CONSTRAINT chk_producto_iva CHECK (iva_porcentaje IN (0,15));

-- 3) FACTURAS COMO CABECERA
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS id_usuario INT;
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVA';
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS forma_pago VARCHAR(10) NOT NULL DEFAULT '01';
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS observaciones VARCHAR(300);
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS motivo_anulacion VARCHAR(300);
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS fecha_anulacion TIMESTAMP;
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS subtotal_sin_impuestos DECIMAL(12,2) NOT NULL DEFAULT 0;
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS base_iva_0 DECIMAL(12,2) NOT NULL DEFAULT 0;
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS base_iva_15 DECIMAL(12,2) NOT NULL DEFAULT 0;
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS iva_15 DECIMAL(12,2) NOT NULL DEFAULT 0;
ALTER TABLE facturas ADD COLUMN IF NOT EXISTS total_descuento DECIMAL(12,2) NOT NULL DEFAULT 0;
ALTER TABLE facturas DROP CONSTRAINT IF EXISTS chk_factura_estado;
ALTER TABLE facturas ADD CONSTRAINT chk_factura_estado CHECK (estado IN ('ACTIVA','ANULADA'));
ALTER TABLE facturas DROP CONSTRAINT IF EXISTS fk_factura_usuario;
ALTER TABLE facturas ADD CONSTRAINT fk_factura_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios(id);

UPDATE facturas
SET subtotal_sin_impuestos = total,
    base_iva_0 = total,
    base_iva_15 = 0,
    iva_15 = 0
WHERE subtotal_sin_impuestos = 0 AND total IS NOT NULL;

-- 4) DETALLE: UNA FACTURA PUEDE TENER VARIOS PRODUCTOS
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

INSERT INTO detalle_factura (
    id_factura, id_producto, cantidad, precio_unitario,
    iva_porcentaje, base_imponible, valor_iva, subtotal
)
SELECT
    f.id_factura, f.id_producto, 1,
    COALESCE(p.precio, f.total), 0,
    f.total, 0, f.total
FROM facturas f
LEFT JOIN productos p ON p.id_producto = f.id_producto
WHERE f.id_producto IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM detalle_factura d WHERE d.id_factura = f.id_factura);

-- 5) TRAZABILIDAD DE INVENTARIO
CREATE TABLE IF NOT EXISTS movimientos_inventario (
    id_movimiento SERIAL PRIMARY KEY,
    id_producto INT NOT NULL REFERENCES productos(id_producto),
    tipo VARCHAR(30) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    stock_anterior INT NOT NULL CHECK (stock_anterior >= 0),
    stock_nuevo INT NOT NULL CHECK (stock_nuevo >= 0),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_factura INT REFERENCES facturas(id_factura),
    id_usuario INT REFERENCES usuarios(id),
    motivo VARCHAR(300) NOT NULL,
    CONSTRAINT chk_movimiento_tipo CHECK (
        tipo IN ('ENTRADA','SALIDA_VENTA','REVERSO_VENTA','AJUSTE_ENTRADA','AJUSTE_SALIDA')
    )
);

CREATE INDEX IF NOT EXISTS idx_detalle_factura ON detalle_factura(id_factura);
CREATE INDEX IF NOT EXISTS idx_detalle_producto ON detalle_factura(id_producto);
CREATE INDEX IF NOT EXISTS idx_movimiento_producto ON movimientos_inventario(id_producto);
CREATE INDEX IF NOT EXISTS idx_movimiento_factura ON movimientos_inventario(id_factura);

-- 6) SECUENCIAL ATÓMICO PARA NUEVAS FACTURAS 001-001-000000001
CREATE SEQUENCE IF NOT EXISTS factura_secuencial_seq START WITH 1 INCREMENT BY 1;
SELECT setval(
    'factura_secuencial_seq',
    GREATEST((SELECT COALESCE(MAX(id_factura), 0) FROM facturas), 1),
    (SELECT COUNT(*) > 0 FROM facturas)
);

-- Se conserva facturas.id_producto por compatibilidad con datos antiguos.

COMMIT;
