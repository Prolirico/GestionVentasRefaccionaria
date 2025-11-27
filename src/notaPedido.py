from dbConnection import get_conn
from datetime import datetime

class NotaPedido:
    def __init__(self, id_, id_usuario, nombre_producto, detalles, fecha):
        self.id = id_
        self.id_usuario = id_usuario
        self.nombre_producto = nombre_producto
        self.detalles = detalles
        self.fecha = fecha

    # Crear una nota de producto faltante
    @classmethod
    def crear(cls, id_usuario, nombre_producto, detalles, fecha=None):
        # Si no se proporciona fecha, usar fecha actual
        if fecha is None:
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
        else:
            fecha_actual = fecha
            
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

            return cls(new_id, id_usuario, nombre_producto, detalles, fecha_actual)

        finally:
            cur.close()
            conn.close()

    # Buscar por ID
    @classmethod
    def buscar_por_id(cls, id_nota):
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
                return None

            return cls(row[0], row[1], row[2], row[3], row[4])

        finally:
            cur.close()
            conn.close()

    # Listar todas las notas
    @classmethod
    def listar_todas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, id_usuario, nombre_producto, detalles, fecha
                FROM notas_productos_faltantes
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
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM notas_productos_faltantes WHERE id = %s", (self.id,))
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"Nota #{self.id} - {self.nombre_producto} ({self.fecha})"
