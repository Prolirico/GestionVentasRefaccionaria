import hashlib
from dbConnection import get_conn

def hash_password(pwd: str):
    if pwd is None:
        return None
    return hashlib.sha256(pwd.encode("utf-8")).hexdigest()

class Usuario:
    CODIGO_ADMIN = "ADMIN123"
    
    def __init__(self, id_, nombre, rol="vendedor"):
        self.id = id_
        self.nombre = nombre
        self.rol = rol

    # CREAR USUARIO CON CODIGO ADMIN
    @classmethod
    def crear(cls, nombre, correo, password, rol="vendedor", codigo_admin=None):
        print(f"[DEBUG] Intentando crear usuario:")
        print(f"        nombre={nombre}, correo={correo}, rol={rol}")

        # Validar si el rol es admin
        if rol == 'administrador':
            if not codigo_admin:
                raise ValueError("Se requiere código de administrador para crear usuarios admin.")
            if codigo_admin != cls.CODIGO_ADMIN:
                raise ValueError("Código de administrador incorrecto.")
            if not password:
                raise ValueError("Los administradores deben tener una contraseña.")

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

            print(f"[DEBUG] Usuario creado exitosamente con ID={uid}")

            return cls(uid, nombre, rol)

        except Exception as e:
            print(f"[ERROR] No se pudo crear el usuario: {e}")
            raise
        finally:
            cur.close()
            conn.close()

    # LISTAR USUARIOS
    @classmethod
    def listar_todos(cls):
        print("[DEBUG] Listando usuarios...")

        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, rol FROM usuarios ORDER BY nombre")

            rows = cur.fetchall()

            if not rows:
                print("[DEBUG] No hay usuarios registrados.")
                return []

            print(f"[DEBUG] Se encontraron {len(rows)} usuarios.")

            return [cls(r[0], r[1], r[2]) for r in rows]

        except Exception as e:
            print(f"[ERROR] Error al listar usuarios: {e}")
            return []

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
                print("[DEBUG] No existe el correo en la base de datos.")
                return None

            stored_hash = row[3]
            if stored_hash == hash_password(password):
                print("[DEBUG] Autenticación correcta.")
                return cls(row[0], row[1], row[2])

            print("[DEBUG] Contraseña incorrecta.")
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

    # ELIMINAR USUARIO (solo para admins)
    def eliminar(self):
        print(f"[DEBUG] Eliminando usuario ID={self.id}")

        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM usuarios WHERE id = %s", (self.id,))
            conn.commit()
            print("[DEBUG] Usuario eliminado correctamente.")
        except Exception as e:
            print(f"[ERROR] Error al eliminar usuario: {e}")
            raise
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.nombre} ({self.rol})"