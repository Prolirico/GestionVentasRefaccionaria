from dbConnection import get_conn

class Producto:
    def __init__(self, id_, nombre, marca, tipo, categoria, version, precio_costo, precio_venta, existencias):
        self.id = id_
        self.nombre = nombre
        self.marca = marca
        self.tipo = tipo
        self.categoria = categoria
        self.version = version
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.existencias = existencias

    # CREAR PRODUCTO
    @classmethod
    def crear(cls, nombre, marca, tipo, categoria, version, precio_costo, precio_venta, existencias):
        print("[DEBUG] Intentando crear producto:")
        print(f"        nombre={nombre}")
        print(f"        marca={marca}")
        print(f"        tipo={tipo}")
        print(f"        categoria={categoria}")
        print(f"        version={version}")
        print(f"        precio_costo={precio_costo}")
        print(f"        precio_venta={precio_venta}")
        print(f"        existencias={existencias}")

        try:
            precio_costo = float(precio_costo)
            precio_venta = float(precio_venta)
            existencias = int(existencias)
        except Exception as e:
            print(f"[ERROR] Conversión fallida: {e}")
            return None

        conn = get_conn()
        try:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO productos
                (nombre, marca, tipo, categoria, tipo_version, precio_costo, precio_venta, existencias)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                nombre, marca, tipo, categoria, version,
                precio_costo, precio_venta, existencias
            ))

            conn.commit()
            pid = cur.lastrowid
            print(f"[DEBUG] Producto creado exitosamente con ID={pid}")

            return cls(pid, nombre, marca, tipo, categoria, version, precio_costo, precio_venta, existencias)

        except Exception as e:
            print(f"[ERROR] No se pudo crear el producto: {e}")
            return None

        finally:
            cur.close()
            conn.close()

    # LISTAR PRODUCTOS
    @classmethod
    def listar_todos(cls):
        print("[DEBUG] Listando productos...")

        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, marca, tipo, categoria, tipo_version, precio_costo, precio_venta, existencias
                FROM productos ORDER BY nombre
            """)

            rows = cur.fetchall()

            if not rows:
                print("[DEBUG] No hay productos registrados.")
                return []

            print(f"[DEBUG] Se encontraron {len(rows)} productos.")

            return [cls(*r) for r in rows]

        except Exception as e:
            print(f"[ERROR] Error al listar productos: {e}")
            return []

        finally:
            cur.close()
            conn.close()
            
    #Buscar Porducto
    @classmethod
    def buscar_por_id(cls, id_producto):
        print(f"[DEBUG] Buscando producto por ID={id_producto}")

        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, marca, tipo, categoria, tipo_version, 
                    precio_costo, precio_venta, existencias
                FROM productos 
                WHERE id = %s
            """, (id_producto,))

            row = cur.fetchone()
            if not row:
                print(f"[DEBUG] Producto con ID {id_producto} no encontrado")
                return None

            print(f"[DEBUG] Producto encontrado: {row[1]}")
            return cls(*row)

        except Exception as e:
            print(f"[ERROR] Error al buscar producto por ID: {e}")
            return None

        finally:
            cur.close()
            conn.close()

    # ACTUALIZAR
    def actualizar(self):
        print(f"[DEBUG] Actualizando producto ID={self.id}")

        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE productos
                SET nombre=%s, marca=%s, tipo=%s, categoria=%s, tipo_version=%s,
                    precio_costo=%s, precio_venta=%s, existencias=%s
                WHERE id=%s
            """, (
                self.nombre, self.marca, self.tipo, self.categoria, self.version,
                self.precio_costo, self.precio_venta, self.existencias, self.id
            ))

            conn.commit()
            print("[DEBUG] Producto actualizado correctamente.")

        except Exception as e:
            print(f"[ERROR] Error al actualizar producto: {e}")

        finally:
            cur.close()
            conn.close()

    # ELIMINAR
    def eliminar(self):
        print(f"[DEBUG] Eliminando producto ID={self.id}")

        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM productos WHERE id=%s", (self.id,))
            conn.commit()
            print("[DEBUG] Producto eliminado correctamente.")

        except Exception as e:
            print(f"[ERROR] Error al eliminar producto: {e}")

        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"{self.nombre} - {self.marca} (${self.precio_venta}) [{self.existencias} unidades]"
