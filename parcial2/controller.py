from model import Database

class Controller:
    def __init__(self):
        self.db = Database()

    def create_producto(self, nombre, descripcion, precio, cantidad, categoria):
        if not nombre or not precio or not cantidad:
            return False, "Todos los campos obligatorios deben estar completos"
        try:
            precio = float(precio)
            cantidad = int(cantidad)
            if precio < 0 or cantidad < 0:
                return False, "El precio y cantidad deben ser valores positivos"
        except ValueError:
            return False, "El precio debe ser numérico y la cantidad un entero"
        
        self.db.insert_producto(nombre, descripcion, precio, cantidad, categoria)
        return True, "Producto registrado exitosamente"

    def get_all_productos(self):
        return self.db.get_all_productos()

    def get_producto(self, id):
        return self.db.get_producto(id)

    def update_producto(self, id, nombre, descripcion, precio, cantidad, categoria):
        if not nombre or not precio or not cantidad:
            return False, "Todos los campos obligatorios deben estar completos"
        try:
            precio = float(precio)
            cantidad = int(cantidad)
            if precio < 0 or cantidad < 0:
                return False, "El precio y cantidad deben ser valores positivos"
        except ValueError:
            return False, "El precio debe ser numérico y la cantidad un entero"
        
        self.db.update_producto(id, nombre, descripcion, precio, cantidad, categoria)
        return True, "Producto actualizado exitosamente"

    def delete_producto(self, id):
        self.db.delete_producto(id)
        return True, "Producto eliminado exitosamente"

    def search_productos(self, criterio):
        if not criterio:
            return self.get_all_productos()
        return self.db.search_productos(criterio)