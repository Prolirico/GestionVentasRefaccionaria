import hashlib
from db_connection import get_conn

def hash_password(pwd: str):
    if pwd is None:
        return None
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()

class Usuario:
    def __init__(self, id_, nombre, rol="vendedor"):
        self.id = id_
        self.nombre = nombre
        self.rol = rol

    @classmethod
    def crear(cls, nombre, correo, password, rol="vendedor"):
        conn = get_conn()
        try:
            cur = conn.cursor()

            pwd_hash = hash_password(password)

            cur.execute("""
                INSERT INTO usuarios (nombre, correo, password, rol)
                VALUES (%s, %s, %s, %s)
            """, (nombre, correo, pwd_hash, rol))

            conn.commit()
            uid = cur.lastrowid
            return cls(uid, nombre, rol)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def autenticar(cls, correo, password):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, rol, password
                FROM usuarios
                WHERE correo = %s
            """, (correo,))

            row = cur.fetchone()
            if not row:
                return None

            stored_hash = row[3]
            if stored_hash == hash_password(password):
                return cls(row[0], row[1], row[2])
            return None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, rol FROM usuarios WHERE id = %s", (id_,))
            row = cur.fetchone()
            return cls(row[0], row[1], row[2]) if row else None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_por_correo(cls, correo):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, rol FROM usuarios WHERE correo = %s", (correo,))
            row = cur.fetchone()
            return cls(row[0], row[1], row[2]) if row else None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, rol FROM usuarios ORDER BY nombre")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2]) for r in rows]
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.nombre} ({self.rol})"
