"""
Command Handler: Eliminar Producto
==================================
CQRS - Manejador del comando DeleteProductoCommand
"""
from parcial2_CQRS.commands.delete_producto import DeleteProductoCommand

class DeleteProductoHandler:
    def __init__(self, db):
        self.db = db
    
    def execute(self, command: DeleteProductoCommand):
        """Ejecuta el command para eliminar producto"""
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (command.id,))
        self.db.commit()
        return cursor.rowcount > 0