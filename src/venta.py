# venta.py
from db_connection import get_conn
from producto import Producto

class Venta:
    def __init__(self, id_, id_usuario, fecha, id_producto, nombre_producto,
                 precio_unitario, cantidad, subtotal, total_venta):
        self.id = id_
        self.id_usuario = id_usuario
        self.fecha = fecha
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.subtotal = subtotal
        self.total_venta = total_venta

    # Crear una venta (y descontar existencias)
    @classmethod
    def crear(cls, id_usuario, fecha, id_producto, cantidad):
        # 1. Cargar producto
        producto = Producto.buscar_por_id(id_producto)
        if not producto:
            raise ValueError("El producto no existe.")

        # 2. Validar stock
        if producto.existencias < cantidad:
            raise ValueError("No hay existencias suficientes para la venta.")

        # 3. Calcular precios
        precio_unitario = producto.precio_venta
        subtotal = precio_unitario * cantidad
        total_venta = subtotal

        # 4. Insertar venta
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO ventas 
                (id_usuario, fecha, id_producto, nombre_producto, precio_unitario,
                 cantidad, subtotal, total_venta)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                id_usuario,
                fecha,
                id_producto,
                producto.nombre,
                precio_unitario,
                cantidad,
                subtotal,
                total_venta
            ))

            conn.commit()
            new_id = cur.lastrowid

        finally:
            cur.close()
            conn.close()

        # 5. Descontar existencias del producto
        producto.existencias -= cantidad
        producto.actualizar()

        return cls(new_id, id_usuario, fecha, id_producto, producto.nombre,
                   precio_unitario, cantidad, subtotal, total_venta)

    # Buscar venta
    @classmethod
    def buscar_por_id(cls, id_venta):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, id_usuario, fecha, id_producto, nombre_producto,
                       precio_unitario, cantidad, subtotal, total_venta
                FROM ventas
                WHERE id = %s
            """, (id_venta,))

            row = cur.fetchone()
            if not row:
                return None

            return cls(*row)

        finally:
            cur.close()
            conn.close()

    # Listar todas las ventas
    @classmethod
    def listar_todas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, id_usuario, fecha, id_producto, nombre_producto,
                       precio_unitario, cantidad, subtotal, total_venta
                FROM ventas
                ORDER BY fecha DESC
            """)

            rows = cur.fetchall()
            return [cls(*r) for r in rows]

        finally:
            cur.close()
            conn.close()

    # Eliminar
    def eliminar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ventas WHERE id = %s", (self.id,))
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"Venta #{self.id}: {self.nombre_producto} x{self.cantidad} (${self.total_venta})"
