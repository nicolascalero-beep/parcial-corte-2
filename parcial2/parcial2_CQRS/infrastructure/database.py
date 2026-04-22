"""
Database: Conexión a SQLite
==========================
CQRS - Capa de acceso a datos
"""
import sqlite3

class Database:
    def __init__(self, db_name="emprendimiento_cqrs.db"):
        self.db_name = db_name
        self._inicializar()
    
    def _inicializar(self):
        """Crea la tabla si no existe"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                categoria TEXT,
                fecha_registro TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)