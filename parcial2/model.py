import sqlite3

class Database:
    def __init__(self, db_name="emprendimiento.db"):
        self.db_name = db_name
        self.create_table()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad INTEGER NOT NULL,
                categoria TEXT,
                fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def insert_producto(self, nombre, descripcion, precio, cantidad, categoria):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria)
            VALUES (?, ?, ?, ?, ?)
        """, (nombre, descripcion, precio, cantidad, categoria))
        conn.commit()
        conn.close()

    def get_all_productos(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id DESC")
        productos = cursor.fetchall()
        conn.close()
        return productos

    def get_producto(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        producto = cursor.fetchone()
        conn.close()
        return producto

    def update_producto(self, id, nombre, descripcion, precio, cantidad, categoria):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, precio = ?, cantidad = ?, categoria = ?
            WHERE id = ?
        """, (nombre, descripcion, precio, cantidad, categoria, id))
        conn.commit()
        conn.close()

    def delete_producto(self, id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        conn.commit()
        conn.close()

    def search_productos(self, criterio):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM productos
            WHERE nombre LIKE ? OR categoria LIKE ?
            ORDER BY id DESC
        """, (f"%{criterio}%", f"%{criterio}%"))
        productos = cursor.fetchall()
        conn.close()
        return productos