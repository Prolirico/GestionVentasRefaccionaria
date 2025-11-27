from dbConnection import get_conn
from producto import Producto

class OrdenCompra:
    def __init__(self, id_, nombre_proveedor, fecha, id_producto, nombre_producto,
                 precio_unitario, cantidad, subtotal, total_orden):
        self.id = id_
        self.nombre_proveedor = nombre_proveedor  # Cambiado a texto
        self.fecha = fecha
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.total_orden = total_orden

    # Crear una orden de compra
    @classmethod
    def crear(cls, nombre_proveedor, fecha, id_producto, cantidad, precio_unitario):
        # Cargar producto
        producto = Producto.buscar_por_id(id_producto)
        if not producto:
            raise ValueError("El producto no existe.")

        # Calcular total
        subtotal = precio_unitario * cantidad
        total_orden = subtotal

        # Guardar en BD
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO ordenes_compra
                (nombre_proveedor, fecha, id_producto, nombre_producto, precio_unitario,
                 cantidad, subtotal, total_orden)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nombre_proveedor, fecha, id_producto, producto.nombre,
                precio_unitario, cantidad, subtotal, total_orden
            ))

            conn.commit()
            new_id = cur.lastrowid

        finally:
            cur.close()
            conn.close()

        # Aumentar existencias
        producto.existencias += cantidad
        producto.actualizar()

        return cls(new_id, nombre_proveedor, fecha, id_producto, producto.nombre,
                   precio_unitario, cantidad, subtotal, total_orden)

    # Buscar
    @classmethod
    def buscar_por_id(cls, id_orden):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, nombre_proveedor, fecha, id_producto, nombre_producto,
                       precio_unitario, cantidad, subtotal, total_orden
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

    # Listar
    @classmethod
    def listar_todas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, nombre_proveedor, fecha, id_producto, nombre_producto,
                       precio_unitario, cantidad, subtotal, total_orden
                FROM ordenes_compra
                ORDER BY fecha DESC
            """)

            rows = cur.fetchall()
            return [cls(*r) for r in rows]

        finally:
            cur.close()
            conn.close()

    # Actualizar
    def actualizar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                UPDATE ordenes_compra
                SET nombre_proveedor = %s,
                    fecha = %s,
                    id_producto = %s,
                    nombre_producto = %s,
                    precio_unitario = %s,
                    cantidad = %s,
                    subtotal = %s,
                    total_orden = %s
                WHERE id = %s
            """, (
                self.nombre_proveedor, self.fecha, self.id_producto,
                self.nombre_producto, self.precio_unitario,
                self.cantidad, self.subtotal, self.total_orden, self.id
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
        return f"Orden #{self.id} - {self.nombre_producto} x{self.cantidad} - {self.nombre_proveedor} (${self.total_orden})"