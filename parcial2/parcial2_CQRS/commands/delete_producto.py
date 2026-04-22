"""
Command: Eliminar Producto
=====================
CQRS - Command para eliminar productos
"""
from dataclasses import dataclass

@dataclass
class DeleteProductoCommand:
    id: int