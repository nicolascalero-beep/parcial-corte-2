import tkinter as tk
from tkinter import messagebox, ttk
from parcial2_DDD.application.services import ProductoService

class ProductoView:
    """
    Presentation Layer: Interfaz gráfica con Tkinter
    Solo maneja presentación, no lógica de negocio
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Inventario - DDD")
        self.root.geometry("950x650")
        
        # Inyección de dependencias: vista conoce al servicio
        self.service = ProductoService()
        self.producto_seleccionado = None
        
        self._crear_widgets()
        self._cargar_productos()
    
    def _crear_widgets(self):
        # Header
        header = tk.Frame(self.root, bg="#1a5276", height=60)
        header.pack(fill=tk.X)
        tk.Label(header, text="Sistema de Gestión de Inventario (DDD)", 
                font=("Arial", 16, "bold"), bg="#1a5276", fg="white").pack(pady=15)
        
        # Formulario
        form = tk.Frame(self.root, bg="#f4f6f7")
        form.pack(fill=tk.X, padx=20, pady=10)
        
        # Fila 1
        tk.Label(form, text="Nombre:", bg="#f4f6f7").grid(row=0, column=0, padx=8, pady=6, sticky="e")
        self.entry_nombre = tk.Entry(form, width=28)
        self.entry_nombre.grid(row=0, column=1, padx=8, pady=6)
        
        tk.Label(form, text="Descripción:", bg="#f4f6f7").grid(row=0, column=2, padx=8, pady=6, sticky="e")
        self.entry_desc = tk.Entry(form, width=28)
        self.entry_desc.grid(row=0, column=3, padx=8, pady=6)
        
        # Fila 2
        tk.Label(form, text="Precio:", bg="#f4f6f7").grid(row=1, column=0, padx=8, pady=6, sticky="e")
        self.entry_precio = tk.Entry(form, width=28)
        self.entry_precio.grid(row=1, column=1, padx=8, pady=6)
        
        tk.Label(form, text="Cantidad:", bg="#f4f6f7").grid(row=1, column=2, padx=8, pady=6, sticky="e")
        self.entry_cant = tk.Entry(form, width=28)
        self.entry_cant.grid(row=1, column=3, padx=8, pady=6)
        
        # Fila 3
        tk.Label(form, text="Categoría:", bg="#f4f6f7").grid(row=2, column=0, padx=8, pady=6, sticky="e")
        self.entry_cat = tk.Entry(form, width=28)
        self.entry_cat.grid(row=2, column=1, padx=8, pady=6)
        
        tk.Label(form, text="Buscar:", bg="#f4f6f7").grid(row=2, column=2, padx=8, pady=6, sticky="e")
        self.entry_buscar = tk.Entry(form, width=28)
        self.entry_buscar.grid(row=2, column=3, padx=8, pady=6)
        tk.Button(form, text="🔍 Buscar", command=self._buscar, bg="#3498db", fg="white").grid(row=2, column=4, padx=8)
        
        # Botones
        btn_frame = tk.Frame(self.root, bg="#f4f6f7")
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
        table_frame = tk.Frame(self.root, bg="#f4f6f7")
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
        """Query: Leer productos del dominio"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            productos = self.service.listar_productos()
            for p in productos:
                valores = (p.id, p.nombre, p.descripcion, f"${p.precio:.2f}", p.cantidad, p.categoria, p.fecha_registro)
                self.tree.insert("", tk.END, values=valores)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar: {str(e)}")
    
    def _crear(self):
        """Command: Crear nuevo producto"""
        try:
            prod = self.service.crear_producto(
                self.entry_nombre.get(),
                self.entry_desc.get(),
                self.entry_precio.get(),
                self.entry_cant.get(),
                self.entry_cat.get()
            )
            messagebox.showinfo("Éxito", f"Producto creado: {prod.id}")
            self._cargar_productos()
            self._limpiar()
        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _actualizar(self):
        """Command: Actualizar producto"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un producto")
            return
        
        try:
            self.service.actualizar_producto(
                self.producto_seleccionado,
                self.entry_nombre.get(),
                self.entry_desc.get(),
                self.entry_precio.get(),
                self.entry_cant.get(),
                self.entry_cat.get()
            )
            messagebox.showinfo("Éxito", "Producto actualizado")
            self._cargar_productos()
            self._limpiar()
        except ValueError as e:
            messagebox.showwarning("Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _eliminar(self):
        """Command: Eliminar producto"""
        if not self.producto_seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un producto")
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar?"):
            try:
                self.service.eliminar_producto(self.producto_seleccionado)
                messagebox.showinfo("Éxito", "Producto eliminado")
                self._cargar_productos()
                self._limpiar()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _buscar(self):
        """Query: Buscar productos"""
        criterio = self.entry_buscar.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            productos = self.service.buscar_productos(criterio) if criterio else self.service.listar_productos()
            for p in productos:
                valores = (p.id, p.nombre, p.descripcion, f"${p.precio:.2f}", p.cantidad, p.categoria, p.fecha_registro)
                self.tree.insert("", tk.END, values=valores)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _seleccionar(self, event):
        """Handler: Seleccionar producto de la tabla"""
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            valores = item["values"]
            
            self.producto_seleccionado = valores[0]
            self.entry_nombre.delete(0, tk.END); self.entry_nombre.insert(0, valores[1])
            self.entry_desc.delete(0, tk.END); self.entry_desc.insert(0, valores[2])
            self.entry_precio.delete(0, tk.END); self.entry_precio.insert(0, valores[3].replace("$", ""))
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