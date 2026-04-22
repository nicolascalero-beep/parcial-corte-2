"""
Queries: Lectura de datos
=======================
CQRS - Todos los Queries del sistema
"""
from parcial2_CQRS.queries.get_all_productos import GetAllProductosQuery
from parcial2_CQRS.queries.get_producto_by_id import GetProductoByIdQuery
from parcial2_CQRS.queries.search_productos import SearchProductosQuery

__all__ = ["GetAllProductosQuery", "GetProductoByIdQuery", "SearchProductosQuery"]