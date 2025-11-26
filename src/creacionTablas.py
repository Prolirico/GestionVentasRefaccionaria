import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

def crear_tablas():
    print("🔧 Creando tablas en MySQL...\n")

    try:
        # Conectar a MySQL
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )

        if conn.is_connected():
            cursor = conn.cursor()
            tablas_sql = [
                # Usuarios
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    rol ENUM('vendedor','administrador') NOT NULL,
                    correo VARCHAR(150) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
                """,

                # Productos
                """
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(150) NOT NULL,
                    marca VARCHAR(100) NOT NULL,
                    tipo ENUM('refaccion','accesorio') NOT NULL,
                    categoria VARCHAR(100),
                    tipo_version VARCHAR(50),
                    precio_costo DECIMAL(10,2) NOT NULL,
                    precio_venta DECIMAL(10,2) NOT NULL,
                    existencias INT NOT NULL DEFAULT 0
                );
                """,

                # Vehículos
                """
                CREATE TABLE IF NOT EXISTS vehiculos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    marca VARCHAR(100) NOT NULL,
                    modelo VARCHAR(100) NOT NULL,
                    anio INT NOT NULL
                );
                """,

                # Compatibilidad Refacción
                """
                CREATE TABLE IF NOT EXISTS compatibilidad_refaccion (
                    id_producto INT NOT NULL,
                    id_vehiculo INT NOT NULL,
                    PRIMARY KEY(id_producto, id_vehiculo),
                    FOREIGN KEY(id_producto) REFERENCES productos(id),
                    FOREIGN KEY(id_vehiculo) REFERENCES vehiculos(id)
                );
                """,

                # Ventas (unificada con detalle)
                """
                CREATE TABLE IF NOT EXISTS ventas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_usuario INT NOT NULL,
                    fecha DATETIME NOT NULL,
                    id_producto INT NOT NULL,
                    nombre_producto VARCHAR(150) NOT NULL,
                    precio_unitario DECIMAL(10,2) NOT NULL,
                    cantidad INT NOT NULL,
                    subtotal DECIMAL(10,2) NOT NULL,
                    total_venta DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id),
                    FOREIGN KEY(id_producto) REFERENCES productos(id)
                );
                """,

                # Proveedores
                """
                CREATE TABLE IF NOT EXISTS proveedores (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(150) NOT NULL,
                    telefono VARCHAR(50),
                    correo VARCHAR(150)
                );
                """,

                # Ordenes de compra
                """
                CREATE TABLE IF NOT EXISTS ordenes_compra (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_proveedor INT NOT NULL,
                    fecha DATETIME NOT NULL,
                    id_producto INT NOT NULL,
                    nombre_producto VARCHAR(150) NOT NULL,
                    precio_unitario DECIMAL(10,2) NOT NULL,
                    cantidad INT NOT NULL,
                    subtotal DECIMAL(10,2) NOT NULL,
                    total_orden DECIMAL(10,2) NOT NULL,
                    estado ENUM('pendiente','completada') NOT NULL,
                    FOREIGN KEY(id_producto) REFERENCES productos(id),
                    FOREIGN KEY(id_proveedor) REFERENCES proveedores(id)
                );
                """,

                # Notas de productos faltantes
                """
                CREATE TABLE IF NOT EXISTS notas_productos_faltantes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    id_usuario INT NOT NULL,
                    nombre_producto VARCHAR(150) NOT NULL,
                    detalles TEXT,
                    fecha DATETIME NOT NULL,
                    FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
                );
                """
            ]
            for tabla in tablas_sql:
                cursor.execute(tabla)

            conn.commit()
            conn.close()

            print("✔ Todas las tablas fueron creadas correctamente.")
            print("🔚 Conexión a MySQL cerrada.\n")

    except Error as e:
        print("❌ ERROR al crear las tablas en MySQL.")
        print(f"Detalles: {e}")


if __name__ == "__main__":
    crear_tablas()
