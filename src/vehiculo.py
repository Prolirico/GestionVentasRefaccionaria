from db_connection import get_conn

class Vehiculo:
    def __init__(self, id_, marca, modelo, anio):
        self.id = id_
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    # Crear vehiculo
    @classmethod
    def crear(cls, marca, modelo, anio):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO vehiculos (marca, modelo, anio)
                VALUES (%s, %s, %s)
            """, (marca, modelo, anio))

            conn.commit()
            vid = cur.lastrowid
            return cls(vid, marca, modelo, anio)

        finally:
            cur.close()
            conn.close()

    # Buscar por ID
    @classmethod
    def buscar_por_id(cls, id_vehiculo):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, marca, modelo, anio
                FROM vehiculos
                WHERE id = %s
            """, (id_vehiculo,))

            row = cur.fetchone()
            if not row:
                return None

            return cls(row[0], row[1], row[2], row[3])

        finally:
            cur.close()
            conn.close()

    # Listar todos
    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, marca, modelo, anio
                FROM vehiculos
                ORDER BY marca, modelo, anio
            """)

            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3]) for r in rows]

        finally:
            cur.close()
            conn.close()

    def actualizar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                UPDATE vehiculos
                SET marca = %s,
                    modelo = %s,
                    anio = %s
                WHERE id = %s
            """, (self.marca, self.modelo, self.anio, self.id))

            conn.commit()

        finally:
            cur.close()
            conn.close()

    def eliminar(self):
        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("DELETE FROM vehiculos WHERE id = %s", (self.id,))
            conn.commit()

        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"
