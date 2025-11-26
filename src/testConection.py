import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "refaccionaria.db")

def test_connection():
    print(f"🔌 Intentando conectar a la base de datos '{DB_NAME}'...\n")

    try:
        conn = sqlite3.connect(DB_NAME)
        print("✔ Conexión exitosa a la base de datos.\n")
        conn.close()
        print("🔚 Conexión cerrada correctamente.")
    except Exception as e:
        print("❌ ERROR: No se pudo conectar a la base de datos.")
        print(f"Detalle: {e}")

if __name__ == "__main__":
    test_connection()
