"""
Handlers: Manejadores de Commands y Queries
========================================
CQRS - Coordina los manejadores
"""
from parcial2_CQRS.handlers.create_handler import CreateProductoHandler
from parcial2_CQRS.handlers.update_handler import UpdateProductoHandler
from parcial2_CQRS.handlers.delete_handler import DeleteProductoHandler
from parcial2_CQRS.handlers.get_all_handler import GetAllProductosHandler
from parcial2_CQRS.handlers.search_handler import SearchProductosHandler

__all__ = [
    "CreateProductoHandler", "UpdateProductoHandler", "DeleteProductoHandler",
    "GetAllProductosHandler", "SearchProductosHandler"
]