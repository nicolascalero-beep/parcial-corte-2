"""
Query: Buscar Productos por criterio
==================================
CQRS - Query para búsqueda con filtro
"""
from dataclasses import dataclass

@dataclass
class SearchProductosQuery:
    criterio: str