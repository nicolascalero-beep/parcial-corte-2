"""
Query Handler: Buscar Productos
=============================
CQRS - Manejador de queries de búsqueda
"""
from parcial2_CQRS.queries.search_productos import SearchProductosQuery
from parcial2_CQRS.queries.get_producto_by_id import GetProductoByIdQuery

class SearchProductosHandler:
    def __init__(self, db):
        self.db = db
    
    def execute_search(self, query: SearchProductosQuery):
        """Busca productos por criterio"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT * FROM productos
            WHERE nombre LIKE ? OR categoria LIKE ?
            ORDER BY id DESC
        """, (f"%{query.criterio}%", f"%{query.criterio}%"))
        return cursor.fetchall()
    
    def execute_by_id(self, query: GetProductoByIdQuery):
        """Obtiene producto por ID"""
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (query.id,))
        return cursor.fetchone()