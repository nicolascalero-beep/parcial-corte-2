"""
Command: Actualizar Producto
============================
CQRS - Command para actualizar productos
"""
from dataclasses import dataclass

@dataclass
class UpdateProductoCommand:
    id: int
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    categoria: str