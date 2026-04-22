"""
Query: Obtener Producto por ID
=============================
CQRS - Query para buscar producto específico
"""
from dataclasses import dataclass

@dataclass
class GetProductoByIdQuery:
    id: int