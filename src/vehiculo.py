from dbConnection import get_conn

class Vehiculo:
    def __init__(self, id_, marca, modelo, anio):
        self.id = id_
        self.marca = marca
        self.modelo = modelo
        self.anio = anio

    # CREAR VEHÍCULO
    @classmethod
    def crear(cls, marca, modelo, anio):
        print("[DEBUG] Intentando crear vehículo:")
        print(f"        marca={marca}, modelo={modelo}, anio={anio}")

        try:
            anio = int(anio)
        except Exception as e:
            print(f"[ERROR] Conversión fallida para año: {e}")
            return None

        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO vehiculos (marca, modelo, anio)
                VALUES (%s, %s, %s)
            """, (marca, modelo, anio))

            conn.commit()
            vid = cur.lastrowid

            print(f"[DEBUG] Vehículo creado exitosamente con ID={vid}")

            return cls(vid, marca, modelo, anio)

        except Exception as e:
            print(f"[ERROR] No se pudo crear el vehículo: {e}")
            return None

        finally:
            cur.close()
            conn.close()

    # BUSCAR POR ID
    @classmethod
    def buscar_por_id(cls, id_vehiculo):
        print(f"[DEBUG] Buscando vehículo por ID={id_vehiculo}")

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
                print("[DEBUG] No se encontró el vehículo.")
                return None

            print(f"[DEBUG] Vehículo encontrado: {row[1]} {row[2]} {row[3]}")
            return cls(row[0], row[1], row[2], row[3])

        except Exception as e:
            print(f"[ERROR] Error al buscar por ID: {e}")
            return None

        finally:
            cur.close()
            conn.close()

    # LISTAR TODOS
    @classmethod
    def listar_todos(cls):
        print("[DEBUG] Listando vehículos...")

        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, marca, modelo, anio
                FROM vehiculos
                ORDER BY marca, modelo, anio
            """)

            rows = cur.fetchall()

            if not rows:
                print("[DEBUG] No hay vehículos registrados.")
                return []

            print(f"[DEBUG] Se encontraron {len(rows)} vehículos.")
            return [cls(r[0], r[1], r[2], r[3]) for r in rows]

        except Exception as e:
            print(f"[ERROR] Error al listar vehículos: {e}")
            return []

        finally:
            cur.close()
            conn.close()

    # ACTUALIZAR
    def actualizar(self):
        print(f"[DEBUG] Actualizando vehículo ID={self.id}")

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
            print("[DEBUG] Vehículo actualizado correctamente.")

        except Exception as e:
            print(f"[ERROR] Error al actualizar vehículo: {e}")

        finally:
            cur.close()
            conn.close()

    # ELIMINAR
    def eliminar(self):
        print(f"[DEBUG] Eliminando vehículo ID={self.id}")

        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("DELETE FROM vehiculos WHERE id = %s", (self.id,))
            conn.commit()

            print("[DEBUG] Vehículo eliminado correctamente.")

        except Exception as e:
            print(f"[ERROR] Error al eliminar vehículo: {e}")

        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"
