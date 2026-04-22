"""
Query Handler: Obtener todos los Productos
=========================================
CQRS - Manejador de la query GetAllProductosQuery
"""
from parcial2_CQRS.queries.get_all_productos import GetAllProductosQuery

class GetAllProductosHandler:
    def __init__(self, db):
        self.db = db
    
    def execute(self, query: GetAllProductosQuery):
        """Ejecuta la query para obtener todos los productos"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM productos ORDER BY id DESC")
        return cursor.fetchall()