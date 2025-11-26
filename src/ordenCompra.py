from db_connection import get_conn
from producto import Producto

class OrdenCompra:
    def __init__(self, id_, id_proveedor, fecha, id_producto, nombre_producto,
                 precio_unitario, cantidad, subtotal, total_orden, estado):
        self.id = id_
        self.id_proveedor = id_proveedor
        self.fecha = fecha
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.total_orden = total_orden
        self.estado = estado

    # Crear una orden de compra (aumenta existencias)
    @classmethod
    def crear(cls, id_proveedor, fecha, id_producto, cantidad, precio_unitario, estado="pendiente"):
        # Cargar producto
        producto = Producto.buscar_por_id(id_producto)
        if not producto:
            raise ValueError("El producto no existe.")

        # Calcular totales
        subtotal = precio_unitario * cantidad
        total_orden = subtotal

        # Guardar en BD
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO ordenes_compra
                (id_proveedor, fecha, id_producto, nombre_producto, precio_unitario,
                 cantidad, subtotal, total_orden, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_proveedor, fecha, id_producto, producto.nombre,
                precio_unitario, cantidad, subtotal, total_orden, estado
            ))

            conn.commit()
            new_id = cur.lastrowid

        finally:
            cur.close()
            conn.close()

        # Aumentar existencias SOLO si el pedido esta completada
        if estado == "completada":
            producto.existencias += cantidad
            producto.actualizar()

        return cls(new_id, id_proveedor, fecha, id_producto, producto.nombre,
                   precio_unitario, cantidad, subtotal, total_orden, estado)

    # Buscar por ID
    @classmethod
    def buscar_por_id(cls, id_orden):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, id_proveedor, fecha, id_producto, nombre_producto,
                       precio_unitario, cantidad, subtotal, total_orden, estado
                FROM ordenes_compra
                WHERE id = %s
            """, (id_orden,))

            row = cur.fetchone()
            if not row:
                return None

            return cls(*row)

        finally:
            cur.close()
            conn.close()

    # Listar todas
    @classmethod
    def listar_todas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, id_proveedor, fecha, id_producto, nombre_producto,
                       precio_unitario, cantidad, subtotal, total_orden, estado
                FROM ordenes_compra
                ORDER BY fecha DESC
            """)

            rows = cur.fetchall()
            return [cls(*r) for r in rows]

        finally:
            cur.close()
            conn.close()

    # Actualizar orden
    def actualizar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                UPDATE ordenes_compra
                SET id_proveedor = %s,
                    fecha = %s,
                    id_producto = %s,
                    nombre_producto = %s,
                    precio_unitario = %s,
                    cantidad = %s,
                    subtotal = %s,
                    total_orden = %s,
                    estado = %s
                WHERE id = %s
            """, (
                self.id_proveedor, self.fecha, self.id_producto,
                self.nombre_producto, self.precio_unitario,
                self.cantidad, self.subtotal, self.total_orden,
                self.estado, self.id
            ))

            conn.commit()

        finally:
            cur.close()
            conn.close()

    # Eliminar orden
    def eliminar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ordenes_compra WHERE id = %s", (self.id,))
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"Orden #{self.id} - {self.nombre_producto} x{self.cantidad} ({self.estado})"
