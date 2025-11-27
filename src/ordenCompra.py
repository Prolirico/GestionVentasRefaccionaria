from dbConnection import get_conn
from producto import Producto

print("Debug: Modulo OrdenCompra cargado")

class OrdenCompra:
    def __init__(self, id_, nombre_proveedor, fecha, id_producto, nombre_producto,
                 precio_unitario, cantidad, subtotal, total_orden):
        print(f"Debug: Creando instancia OrdenCompra - ID: {id_}, Producto: {nombre_producto}")
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
        print(f"Debug: Creando nueva orden - Proveedor: {nombre_proveedor}, Producto ID: {id_producto}")
        print(f"Debug: Cantidad: {cantidad}, Precio unitario: {precio_unitario}")
        
        # Cargar producto
        producto = Producto.buscar_por_id(id_producto)
        if not producto:
            error_msg = f"Debug: Producto no encontrado - ID: {id_producto}"
            print(error_msg)
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
            print(f"Debug: Orden creada exitosamente - ID: {new_id}")

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
        print(f"Debug: Buscando orden por ID: {id_orden}")
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
                print(f"Debug: Orden no encontrada - ID: {id_orden}")
                return None

            print(f"Debug: Orden encontrada - ID: {row[0]}, Producto: {row[4]}")
            return cls(*row)

        finally:
            cur.close()
            conn.close()

    # Listar
    @classmethod
    def listar_todas(cls):
        print("Debug: Listando todas las ordenes de compra")
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
            print(f"Debug: Se encontraron {len(rows)} ordenes")
            return [cls(*r) for r in rows]

        finally:
            cur.close()
            conn.close()

    # Actualizar
    def actualizar(self):
        print(f"Debug: Actualizando orden - ID: {self.id}")
        print(f"Debug: Nuevos datos - Producto: {self.nombre_producto}, Cantidad: {self.cantidad}")
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
        print(f"Debug: Eliminando orden - ID: {self.id}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM ordenes_compra WHERE id = %s", (self.id,))
            conn.commit()
            print(f"Debug: Orden eliminada exitosamente - ID: {self.id}")
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"Orden #{self.id} - {self.nombre_producto} x{self.cantidad} - {self.nombre_proveedor} (${self.total_orden})"
    
    def __del__(self):
        print(f"Debug: Instancia OrdenCompra {self.id} siendo destruida")