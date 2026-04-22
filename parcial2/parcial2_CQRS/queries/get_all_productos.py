"""
Query: Obtener todos los Productos
================================
CQRS - Query para leer todos los productos
"""
from dataclasses import dataclass

@dataclass
class GetAllProductosQuery:
    pass