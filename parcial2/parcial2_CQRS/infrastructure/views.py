"""
View: Interfaz Gráfica Tkinter
=============================
CQRS - Presentación con el patrón CQRS
"""
import tkinter as tk
from tkinter import messagebox, ttk
from parcial2_CQRS.commands import CreateProductoCommand, UpdateProductoCommand, DeleteProductoCommand
from parcial2_CQRS.queries import GetAllProductosQuery, SearchProductosQuery, GetProductoByIdQuery
from parcial2_CQRS.infrastructure.bus import CommandQueryBus

class ProductoView:
    """
    View: Capa de presentación
    Usa el CommandQueryBus para enviar Commands y Queries
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Inventario - CQRS")
        self.root.geometry("950x650")
        
        # Bus CQRS compartido
        self.bus = CommandQueryBus()
        self.producto_seleccionado = None
        
        self._crear_widgets()
        self._cargar_productos()
    
    def _crear_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#6a0dad", height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="Sistema de Gestión de Inventario (CQRS)", 
                font=("Arial", 16, "bold"), bg="#6a0dad", fg="white").pack(pady=15)
        
        # Formulario
        form = tk.Frame(self.root, bg="#f5f5f5")
        form.pack(fill=tk.X, padx=20, pady=10)
        
        # Fila 1
        tk.Label(form, text="Nombre:", bg="#f5f5f5").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.entry_nombre = tk.Entry(form, width=28)
        self.entry_nombre.grid(row=0, column=1, padx=8, pady=6)
        
        tk.Label(form, text="Descripción:", bg="#f5f5f5").grid(row=0, column=2, padx=8, pady=6, sticky="e")
        self.entry_desc = tk.Entry(form, width=28)
        self.entry_desc.grid(row=0, column=3, padx=8, pady=6)
        
        # Fila 2
        tk.Label(form, text="Precio:", bg="#f5f5f5").grid(row=1, column=0, padx=8, pady=6, sticky="e")
        self.entry_precio = tk.Entry(form, width=28)
        self.entry_precio.grid(row=1, column=1, padx=8, pady=6)
        
        tk.Label(form, text="Cantidad:", bg="#f5f5f5").grid(row=1, column=2, padx=8, pady=6, sticky="e")
        self.entry_cant = tk.Entry(form, width=28)
        self.entry_cant.grid(row=1, column=3, padx=8, pady=6)
        
        # Fila 3
        tk.Label(form, text="Categoría:", bg="#f5f5f5").grid(row=2, column=0, padx=8, pady=6, sticky="e")
        self.entry_cat = tk.Entry(form, width=28)
        self.entry_cat.grid(row=2, column=1, padx=8, pady=6)
        
        tk.Label(form, text="Buscar:", bg="#f5f5f5").grid(row=2, column=2, padx=8, pady=6, sticky="e")
        self.entry_buscar = tk.Entry(form, width=28)
        self.entry_buscar.grid(row=2, column=3, padx=8, pady=6)
        tk.Button(form, text="🔍 Buscar", command=self._buscar, bg="#9b59b6", fg="white").grid(row=2, column=4, padx=8)
        
        # Botones
        btn_frame = tk.Frame(self.root, bg="#f5f5f5")
        btn_frame.pack(fill=tk.X, padx=20)
        
        tk.Button(btn_frame, text="➕ Nuevo", command=self._crear, bg="#27ae60", fg="white", 
                width=14, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frame, text="✏️ Actualizar", command=self._actualizar, bg="#f39c12", fg="white", 
                width=14, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frame, text="🗑️ Eliminar", command=self._eliminar, bg="#e74c3c", fg="white", 
                width=14, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=6)
        tk.Button(btn_frame, text="🔄 Limpiar", command=self._limpiar, bg="#7f8c8d", fg="white", 
                width=14, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=6)
        
        # Tabla
        table_frame = tk.Frame(self.root, bg="#f5f5f5")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cols = ("ID", "Nombre", "Descripción", "Precio", "Cantidad", "Categoría", "Fecha")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
        
        for col in cols:
            self.tree.heading(col, text=col)
            w = 50 if col == "ID" else 130
            self.tree.column(col, width=w)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self._seleccionar)
    
    def _cargar_productos(self):
        """Query: Obtiene todos los productos"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            query = GetAllProductosQuery()
            productos = self.bus.execute_get_all(query)
            for p in productos:
                self.tree.insert("", tk.END, values=p)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _crear(self):
        """Command: Crea nuevo producto"""
        try:
            command = CreateProductoCommand(
                nombre=self.entry_nombre.get(),
                descripcion=self.entry_desc.get(),
                precio=float(self.entry_precio.get()),
                cantidad=int(self.entry_cant.get()),
                categoria=self.entry_cat.get()
            )
            self.bus.execute_create(command)
            messagebox.showinfo("Éxito", "Producto creado")
            self._cargar_productos()
            self._limpiar()
        except ValueError:
            messagebox.showwarning("Validación", "Precio y cantidad deben ser numéricos")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _actualizar(self):
        """Command: Actualiza producto"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un producto")
            return
        
        try:
            command = UpdateProductoCommand(
                id=self.producto_seleccionado,
                nombre=self.entry_nombre.get(),
                descripcion=self.entry_desc.get(),
                precio=float(self.entry_precio.get()),
                cantidad=int(self.entry_cant.get()),
                categoria=self.entry_cat.get()
            )
            self.bus.execute_update(command)
            messagebox.showinfo("Éxito", "Producto actualizado")
            self._cargar_productos()
            self._limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _eliminar(self):
        """Command: Elimina producto"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un producto")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar?"):
            try:
                command = DeleteProductoCommand(id=self.producto_seleccionado)
                self.bus.execute_delete(command)
                messagebox.showinfo("��xito", "Producto eliminado")
                self._cargar_productos()
                self._limpiar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _buscar(self):
        """Query: Busca productos"""
        criterio = self.entry_buscar.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if criterio:
                query = SearchProductosQuery(criterio=criterio)
                productos = self.bus.execute_search(query)
            else:
                query = GetAllProductosQuery()
                productos = self.bus.execute_get_all(query)
            
            for p in productos:
                self.tree.insert("", tk.END, values=p)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _seleccionar(self, event):
        """Seleccionar producto de la tabla"""
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            valores = item["values"]
            
            self.producto_seleccionado = valores[0]
            self.entry_nombre.delete(0, tk.END); self.entry_nombre.insert(0, valores[1])
            self.entry_desc.delete(0, tk.END); self.entry_desc.insert(0, valores[2])
            self.entry_precio.delete(0, tk.END); self.entry_precio.insert(0, valores[3])
            self.entry_cant.delete(0, tk.END); self.entry_cant.insert(0, valores[4])
            self.entry_cat.delete(0, tk.END); self.entry_cat.insert(0, valores[5])
    
    def _limpiar(self):
        """Limpiar formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_cant.delete(0, tk.END)
        self.entry_cat.delete(0, tk.END)
        self.producto_seleccionado = None