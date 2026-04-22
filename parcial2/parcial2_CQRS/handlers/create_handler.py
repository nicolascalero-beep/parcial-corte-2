"""
Command Handler: Crear Producto
===============================
CQRS - Manejador del comando CreateProductoCommand
"""
from datetime import datetime
from parcial2_CQRS.commands.create_producto import CreateProductoCommand

class CreateProductoHandler:
    def __init__(self, db):
        self.db = db
    
    def execute(self, command: CreateProductoCommand):
        """Ejecuta el command para crear producto"""
        cursor = self.db.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (command.nombre, command.descripcion, command.precio, 
              command.cantidad, command.categoria, fecha))
        self.db.commit()
        return cursor.lastrowid