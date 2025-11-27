from dbConnection import get_conn
from producto import Producto

print("Debug: Modulo Venta cargado")

class Venta:
    def __init__(self, id_, id_usuario, fecha, id_producto, nombre_producto,
                 precio_unitario, cantidad, subtotal, total_venta):
        print(f"Debug: Creando instancia Venta - ID: {id_}, Producto: {nombre_producto}")
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
        print(f"Debug: Creando venta - Usuario: {id_usuario}, Producto: {id_producto}")
        print(f"Debug: Cantidad: {cantidad}, Fecha: {fecha}")
        
        # Cargar producto
        producto = Producto.buscar_por_id(id_producto)
        if not producto:
            print(f"Debug: Producto no encontrado - ID: {id_producto}")
            raise ValueError("El producto no existe.")

        # Validar stock
        if producto.existencias < cantidad:
            print(f"Debug: Stock insuficiente - Disponible: {producto.existencias}, Solicitado: {cantidad}")
            raise ValueError("No hay existencias suficientes para la venta.")

        # Calcular precios
        precio_unitario = producto.precio_venta
        subtotal = precio_unitario * cantidad
        total_venta = subtotal

        # Insertar venta
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
            print(f"Debug: Venta registrada - ID: {new_id}")

        finally:
            cur.close()
            conn.close()

        # Descontar existencias del producto
        producto.existencias -= cantidad
        producto.actualizar()

        return cls(new_id, id_usuario, fecha, id_producto, producto.nombre,
                   precio_unitario, cantidad, subtotal, total_venta)

    # Buscar venta
    @classmethod
    def buscar_por_id(cls, id_venta):
        print(f"Debug: Buscando venta - ID: {id_venta}")
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
                print(f"Debug: Venta no encontrada - ID: {id_venta}")
                return None

            print(f"Debug: Venta encontrada - ID: {row[0]}, Producto: {row[4]}")
            return cls(*row)

        finally:
            cur.close()
            conn.close()

    # Listar todas las ventas
    @classmethod
    def listar_todas(cls):
        print("Debug: Listando todas las ventas")
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
            print(f"Debug: Se encontraron {len(rows)} ventas")
            return [cls(*r) for r in rows]

        finally:
            cur.close()
            conn.close()

    # Eliminar
    def eliminar(self):
        print(f"Debug: Eliminando venta - ID: {self.id}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ventas WHERE id = %s", (self.id,))
            conn.commit()
            print(f"Debug: Venta eliminada - ID: {self.id}")
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"Venta #{self.id}: {self.nombre_producto} x{self.cantidad} (${self.total_venta})"
    
    def __del__(self):
        print(f"Debug: Instancia Venta {self.id} siendo destruida")
