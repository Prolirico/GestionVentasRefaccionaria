CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('vendedor', 'administrador')),
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    marca TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('refaccion', 'accesorio')),
    categoria TEXT,
    tipo_version TEXT,
    precio_costo REAL NOT NULL,
    precio_venta REAL NOT NULL,
    existencias INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS vehiculos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    anio INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS compatibilidad_refaccion (
    id_producto INTEGER NOT NULL,
    id_vehiculo INTEGER NOT NULL,
    PRIMARY KEY(id_producto, id_vehiculo),
    FOREIGN KEY(id_producto) REFERENCES productos(id),
    FOREIGN KEY(id_vehiculo) REFERENCES vehiculos(id)
);

CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    id_producto INTEGER NOT NULL,
    nombre_producto TEXT NOT NULL,
    precio_unitario REAL NOT NULL,
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    total_venta REAL NOT NULL,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY(id_producto) REFERENCES productos(id)
);

CREATE TABLE IF NOS EXISTS ordenes_compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_proveedor VARCHAR(150) NOT NULL,
    fecha TEXT NOT NULL,
    id_producto INTEGER NOT NULL,
    nombre_producto TEXT NOT NULL,
    precio_unitario REAL NOT NULL,
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    total_orden REAL NOT NULL,
    estado TEXT NOT NULL CHECK(estado IN ('pendiente','completada')),
    FOREIGN KEY(id_producto) REFERENCES productos(id),
    FOREIGN KEY(id_proveedor) REFERENCES proveedores(id)
);

CREATE TABLE IF NOT EXISTS detalle_orden_compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_orden INTEGER NOT NULL,
    id_producto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY(id_orden) REFERENCES ordenes_compra(id),
    FOREIGN KEY(id_producto) REFERENCES productos(id)
);

CREATE TABLE IF NOT EXISTS notas_productos_faltantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    nombre_producto TEXT NOT NULL,
    detalles TEXT,
    fecha TEXT NOT NULL,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);
