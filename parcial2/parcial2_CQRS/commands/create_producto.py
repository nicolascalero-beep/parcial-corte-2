"""
Command: Crear Producto
=================
CQRS - Command para crear nuevos productos
"""
from dataclasses import dataclass

@dataclass
class CreateProductoCommand:
    nombre: str
    descripcion: str
    precio: float
    cantidad: int
    categoria: str