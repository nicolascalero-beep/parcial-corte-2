"""
Command Handler: Actualizar Producto
====================================
CQRS - Manejador del comando UpdateProductoCommand
"""
from parcial2_CQRS.commands.update_producto import UpdateProductoCommand

class UpdateProductoHandler:
    def __init__(self, db):
        self.db = db
    
    def execute(self, command: UpdateProductoCommand):
        """Ejecuta el command para actualizar producto"""
        cursor = self.db.cursor()
        cursor.execute("""
            UPDATE productos
            SET nombre = ?, descripcion = ?, precio = ?, cantidad = ?, categoria = ?
            WHERE id = ?
        """, (command.nombre, command.descripcion, command.precio,
              command.cantidad, command.categoria, command.id))
        self.db.commit()
        return cursor.rowcount > 0