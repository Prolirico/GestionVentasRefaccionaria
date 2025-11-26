from db_connection import get_conn

class Producto:
    def __init__(
        self,
        id_,
        nombre,
        marca,
        tipo,
        precio_costo,
        precio_venta,
        existencias,
        categoria=None,
        tipo_version=None
    ):
        self.id = id_
        self.nombre = nombre
        self.marca = marca
        self.tipo = tipo
        self.categoria = categoria
        self.tipo_version = tipo_version
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.existencias = existencias

    # Crear un producto
    @classmethod
    def crear(cls, nombre, marca, tipo, precio_costo, precio_venta,
              existencias=0, categoria=None, tipo_version=None):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO productos 
                (nombre, marca, tipo, categoria, tipo_version, precio_costo, precio_venta, existencias)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombre, marca, tipo, categoria, tipo_version,
                  precio_costo, precio_venta, existencias))

            conn.commit()

            new_id = cur.lastrowid
            return cls(new_id, nombre, marca, tipo, precio_costo, precio_venta,
                       existencias, categoria, tipo_version)

        finally:
            cur.close()
            conn.close()

    # Buscar por ID
    @classmethod
    def buscar_por_id(cls, id_producto):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, marca, tipo, categoria, tipo_version,
                       precio_costo, precio_venta, existencias
                FROM productos
                WHERE id = %s
            """, (id_producto,))

            row = cur.fetchone()
            if not row:
                return None

            return cls(
                id_=row[0],
                nombre=row[1],
                marca=row[2],
                tipo=row[3],
                categoria=row[4],
                tipo_version=row[5],
                precio_costo=row[6],
                precio_venta=row[7],
                existencias=row[8]
            )
        finally:
            cur.close()
            conn.close()

    # Listar todos los productos
    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, marca, tipo, categoria, tipo_version,
                       precio_costo, precio_venta, existencias
                FROM productos
                ORDER BY nombre
            """)

            rows = cur.fetchall()
            return [
                cls(
                    id_=r[0],
                    nombre=r[1],
                    marca=r[2],
                    tipo=r[3],
                    categoria=r[4],
                    tipo_version=r[5],
                    precio_costo=r[6],
                    precio_venta=r[7],
                    existencias=r[8]
                )
                for r in rows
            ]
        finally:
            cur.close()
            conn.close()

    # Actualizar producto
    def actualizar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                UPDATE productos
                SET nombre = %s,
                    marca = %s,
                    tipo = %s,
                    categoria = %s,
                    tipo_version = %s,
                    precio_costo = %s,
                    precio_venta = %s,
                    existencias = %s
                WHERE id = %s
            """, (
                self.nombre, self.marca, self.tipo, self.categoria,
                self.tipo_version, self.precio_costo, self.precio_venta,
                self.existencias, self.id
            ))

            conn.commit()
        finally:
            cur.close()
            conn.close()

    # Eliminar producto
    def eliminar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("DELETE FROM productos WHERE id = %s", (self.id,))
            conn.commit()

        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.nombre} - ${self.precio_venta} ({self.existencias} en stock)"
