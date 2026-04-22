"""
Command Query Bus: Dispara Commands y Queries
============================================
CQRS - Punto central de coordinación
"""
from parcial2_CQRS.infrastructure.database import Database

class CommandQueryBus:
    """
    Bus: Coordina Commands y Queries hacia sus manejadores
    Separa claramente escritura (Commands) de lectura (Queries)
    """
    def __init__(self):
        self.db = Database()
        self._registrar_handlers()
    
    def _registrar_handlers(self):
        """Registra los manejadores disponibles"""
        from parcial2_CQRS.handlers import (
            CreateProductoHandler, UpdateProductoHandler, DeleteProductoHandler,
            GetAllProductosHandler, SearchProductosHandler
        )
        
        self.create_handler = CreateProductoHandler(self.db.get_connection())
        self.update_handler = UpdateProductoHandler(self.db.get_connection())
        self.delete_handler = DeleteProductoHandler(self.db.get_connection())
        self.get_all_handler = GetAllProductosHandler(self.db.get_connection())
        self.search_handler = SearchProductosHandler(self.db.get_connection())
    
    # ========== COMMANDS (Escritura) ==========
    
    def execute_create(self, command):
        """Command: Crear"""
        return self.create_handler.execute(command)
    
    def execute_update(self, command):
        """Command: Actualizar"""
        return self.update_handler.execute(command)
    
    def execute_delete(self, command):
        """Command: Eliminar"""
        return self.delete_handler.execute(command)
    
    # ========== QUERIES (Lectura) ==========
    
    def execute_get_all(self, query):
        """Query: Obtener todos"""
        return self.get_all_handler.execute(query)
    
    def execute_search(self, query):
        """Query: Buscar"""
        return self.search_handler.execute_search(query)
    
    def execute_by_id(self, query):
        """Query: Por ID"""
        return self.search_handler.execute_by_id(query)