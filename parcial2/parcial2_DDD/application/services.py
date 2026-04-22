from parcial2_DDD.dominio.entities import Producto
from parcial2_DDD.dominio.repositories import ProductoRepositorio

class ProductoService:
    """
    Domain Service: Encapsula lógica de negocio del dominio
    Coordina operaciones entre entidades y repositorios
    No都属于dominio, no infraestructura
    """
    def __init__(self):
        self.repositorio = ProductoRepositorio()
    
    def crear_producto(self, nombre, descripcion, precio, cantidad, categoria):
        """
        Service Method: Crear nuevo producto con validaciones de dominio
        """
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio=float(precio),
            cantidad=int(cantidad),
            categoria=categoria
        )
        return self.repositorio.guardar(producto)
    
    def actualizar_producto(self, id, nombre, descripcion, precio, cantidad, categoria):
        """
        Service Method: Actualizar producto existente
        """
        producto_existente = self.repositorio.buscar_por_id(id)
        if not producto_existente:
            raise ValueError(f"Producto con ID {id} no encontrado")
        
        producto = Producto(
            id=id,
            nombre=nombre,
            descripcion=descripcion,
            precio=float(precio),
            cantidad=int(cantidad),
            categoria=categoria,
            fecha_registro=producto_existente.fecha_registro
        )
        return self.repositorio.actualizar(producto)
    
    def eliminar_producto(self, id):
        """Service Method: Eliminar producto"""
        producto = self.repositorio.buscar_por_id(id)
        if not producto:
            raise ValueError(f"Producto con ID {id} no encontrado")
        self.repositorio.eliminar(id)
    
    def obtener_producto(self, id):
        """Service Method: Obtener producto por ID"""
        return self.repositorio.buscar_por_id(id)
    
    def listar_productos(self):
        """Service Method: Listar todos los productos"""
        return self.repositorio.buscar_todos()
    
    def buscar_productos(self, criterio):
        """Service Method: Buscar productos por criterio"""
        return self.repositorio.buscar_por_criterio(criterio)
    
    def validar_datos(self, nombre, precio, cantidad):
        """
        Domain Logic: Validaciones de reglas de negocio
        """
        if not nombre:
            raise ValueError("El nombre es obligatorio")
        if float(precio) < 0:
            raise ValueError("El precio no puede ser negativo")
        if int(cantidad) < 0:
            raise ValueError("La cantidad no puede ser negativa")
        return True