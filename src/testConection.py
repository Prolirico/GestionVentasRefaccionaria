import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

def test_connection():
    print("🔌 Probando conexión a MySQL...\n")

    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )

        if conn.is_connected():
            print("✔ Conexión exitosa a la base de datos MySQL.")
            print(f"📁 Base de datos: {os.getenv('DB_NAME')}")
            print(f"👤 Usuario: {os.getenv('DB_USER')}\n")

            conn.close()
            print("🔚 Conexión cerrada correctamente.")
        else:
            print("❌ No se pudo conectar, pero no arrojó error específico.")

    except Error as error:
        print("❌ ERROR: No se pudo conectar a MySQL.")
        print(f"Detalles: {error}")

if __name__ == "__main__":
    test_connection()
