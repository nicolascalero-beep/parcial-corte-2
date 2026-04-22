import sqlite3
from parcial2_DDD.dominio.entities import Producto

class ProductoRepositorio:
    """
    Repository: Abstracción de la capa de datos
    Maneja la persistencia de entidades Producto
    """
    def __init__(self, db_name="emprendimiento_ddd.db"):
        self.db_name = db_name
        self._crear_tabla()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def _crear_tabla(self):
        conn = self._get_connection()
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
    
    def guardar(self, producto):
        """Guarda una nueva entidad producto"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (producto.nombre, producto.descripcion, producto.precio, 
             producto.cantidad, producto.categoria, producto.fecha_registro))
        producto.id = cursor.lastrowid
        conn.commit()
        conn.close()
        return producto
    
    def actualizar(self, producto):
        """Actualiza una entidad existente"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, precio = ?, cantidad = ?, categoria = ?
            WHERE id = ?
        """, (producto.nombre, producto.descripcion, producto.precio,
              producto.cantidad, producto.categoria, producto.id))
        conn.commit()
        conn.close()
        return producto
    
    def eliminar(self, id):
        """Elimina una entidad por su ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        conn.commit()
        conn.close()
    
    def buscar_por_id(self, id):
        """Busca una entidad por su ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return self._mapear_row_a_entity(row)
        return None
    
    def buscar_todos(self):
        """Busca todas las entidades"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        return [self._mapear_row_a_entity(row) for row in rows]
    
    def buscar_por_criterio(self, criterio):
        """Busca entidades por criterio de búsqueda"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM productos
            WHERE nombre LIKE ? OR categoria LIKE ?
            ORDER BY id DESC
        """, (f"%{criterio}%", f"%{criterio}%"))
        rows = cursor.fetchall()
        conn.close()
        return [self._mapear_row_a_entity(row) for row in rows]
    
    def _mapear_row_a_entity(self, row):
        """Mapea una fila de base de datos a entidad Producto"""
        return Producto(
            id=row[0],
            nombre=row[1],
            descripcion=row[2],
            precio=row[3],
            cantidad=row[4],
            categoria=row[5],
            fecha_registro=row[6]
        )