from dbConnection import get_conn
from datetime import datetime

print("Debug: NotaPedido module loaded")

class NotaPedido:
    def __init__(self, id_, id_usuario, nombre_producto, detalles, fecha):
        print(f"Debug: Creating NotaPedido instance - ID: {id_}, Producto: {nombre_producto}")
        self.id = id_
        self.id_usuario = id_usuario
        self.nombre_producto = nombre_producto
        self.detalles = detalles
        self.fecha = fecha

    # Crear una nota de producto faltante
    @classmethod
    def crear(cls, id_usuario, nombre_producto, detalles, fecha=None):
        print(f"Debug: Creando nueva nota - Usuario: {id_usuario}, Producto: {nombre_producto}")
        print(f"Debug: Detalles: {detalles}")
        
        # Si no se proporciona fecha, usar fecha actual
        if fecha is None:
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            print(f"Debug: Usando fecha actual: {fecha_actual}")
        else:
            fecha_actual = fecha
            print(f"Debug: Usando fecha proporcionada: {fecha_actual}")
            
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO notas_productos_faltantes
                (id_usuario, nombre_producto, detalles, fecha)
                VALUES (%s, %s, %s, %s)
            """, (id_usuario, nombre_producto, detalles, fecha_actual))

            conn.commit()
            new_id = cur.lastrowid
            print(f"Debug: Nota creada exitosamente - ID: {new_id}")

            return cls(new_id, id_usuario, nombre_producto, detalles, fecha_actual)

        finally:
            cur.close()
            conn.close()

    # Buscar por ID
    @classmethod
    def buscar_por_id(cls, id_nota):
        print(f"Debug: Buscando nota por ID: {id_nota}")
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, id_usuario, nombre_producto, detalles, fecha
                FROM notas_productos_faltantes
                WHERE id = %s
            """, (id_nota,))

            row = cur.fetchone()
            if not row:
                print(f"Debug: No se encontro nota con ID: {id_nota}")
                return None

            print(f"Debug: Nota encontrada - ID: {row[0]}, Producto: {row[2]}")
            return cls(row[0], row[1], row[2], row[3], row[4])

        finally:
            cur.close()
            conn.close()

    # Listar todas las notas
    @classmethod
    def listar_todas(cls):
        print("Debug: Listando todas las notas de pedido")
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, id_usuario, nombre_producto, detalles, fecha
                FROM notas_productos_faltantes
                ORDER BY fecha DESC
            """)

            rows = cur.fetchall()
            print(f"Debug: Se encontraron {len(rows)} notas")
            return [cls(*r) for r in rows]

        finally:
            cur.close()
            conn.close()

    # Actualizar
    def actualizar(self):
        print(f"Debug: Actualizando nota - ID: {self.id}")
        print(f"Debug: Nuevos datos - Producto: {self.nombre_producto}, Detalles: {self.detalles}")
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                UPDATE notas_productos_faltantes
                SET id_usuario = %s,
                    nombre_producto = %s,
                    detalles = %s,
                    fecha = %s
                WHERE id = %s
            """, (
                self.id_usuario, self.nombre_producto, self.detalles,
                self.fecha, self.id
            ))

            conn.commit()

        finally:
            cur.close()
            conn.close()

    # Eliminar nota
    def eliminar(self):
        print(f"Debug: Eliminando nota - ID: {self.id}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM notas_productos_faltantes WHERE id = %s", (self.id,))
            conn.commit()
            print(f"Debug: Nota eliminada exitosamente - ID: {self.id}")
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"Nota #{self.id} - {self.nombre_producto} ({self.fecha})"

    def __del__(self):
        print(f"Debug: NotaPedido instance {self.id} is being destroyed")
