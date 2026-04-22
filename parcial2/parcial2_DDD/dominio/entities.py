from datetime import datetime

class Producto:
    """
    Entity: Representa la entidad principal del dominio
    Tiene identidad única yifecycle propio
    """
    def __init__(self, nombre, descripcion, precio, cantidad, categoria, id=None, fecha_registro=None):
        self.id = id
        self._nombre = nombre
        self._descripcion = descripcion
        self._precio = precio
        self._cantidad = cantidad
        self._categoria = categoria
        self._fecha_registro = fecha_registro or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        if not value:
            raise ValueError("El nombre no puede estar vacío")
        self._nombre = value
    
    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, value):
        if value < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = value
    
    @property
    def cantidad(self):
        return self._cantidad
    
    @cantidad.setter
    def cantidad(self, value):
        if value < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self._cantidad = value
    
    @property
    def descripcion(self):
        return self._descripcion
    
    @property
    def categoria(self):
        return self._categoria
    
    @property
    def fecha_registro(self):
        return self._fecha_registro
    
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "precio": self._precio,
            "cantidad": self._cantidad,
            "categoria": self._categoria,
            "fecha_registro": self._fecha_registro
        }


class Precio:
    """
    Value Object: Inmutable, define valor con reglas de negocio
    """
    def __init__(self, monto):
        if monto < 0:
            raise ValueError("El precio no puede ser negativo")
        self._monto = round(monto, 2)
    
    @property
    def monto(self):
        return self._monto
    
    def __repr__(self):
        return f"${self._monto:.2f}"


class Categoria:
    """
    Value Object: Categoría del producto
    """
    CATEGORIAS_VALIDAS = ["Electrónica", "Ropa", "Alimentos", "Hogar", "Deportes", "Otro"]
    
    def __init__(self, nombre):
        self._nombre = nombre
    
    @property
    def nombre(self):
        return self._nombre
    
    def es_valida(self):
        return self._nombre in self.CATEGORIAS_VALIDAS
    
    def __repr__(self):
        return self._nombre