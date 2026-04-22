import tkinter as tk
from tkinter import messagebox, ttk
from controller import Controller

class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Inventario - Emprendimiento")
        self.root.geometry("900x600")
        
        self.controller = Controller()
        self.producto_seleccionado = None
        
        self.create_widgets()
        self.load_productos()

    def create_widgets(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        title_frame.pack(fill=tk.X)
        
        lbl_title = tk.Label(title_frame, text="Sistema de Gestión de Inventario", 
                         font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
        lbl_title.pack(pady=10)

        form_frame = tk.Frame(self.root, bg="#ecf0f1")
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(form_frame, text="Nombre:", bg="#ecf0f1").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nombre = tk.Entry(form_frame, width=25)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Descripción:", bg="#ecf0f1").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.entry_descripcion = tk.Entry(form_frame, width=25)
        self.entry_descripcion.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Precio:", bg="#ecf0f1").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_precio = tk.Entry(form_frame, width=25)
        self.entry_precio.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Cantidad:", bg="#ecf0f1").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.entry_cantidad = tk.Entry(form_frame, width=25)
        self.entry_cantidad.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Categoría:", bg="#ecf0f1").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_categoria = tk.Entry(form_frame, width=25)
        self.entry_categoria.grid(row=2, column=1, padx=5, pady=5)

        self.entry_buscar = tk.Entry(form_frame, width=25)
        self.entry_buscar.grid(row=2, column=2, padx=5, pady=5)
        tk.Button(form_frame, text="Buscar", command=self.buscar_productos, bg="#3498db", fg="white").grid(row=2, column=3, padx=5, pady=5)

        btn_frame = tk.Frame(self.root, bg="#ecf0f1")
        btn_frame.pack(fill=tk.X, padx=20)

        tk.Button(btn_frame, text="Nuevo", command=self.nuevo_producto, bg="#27ae60", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Actualizar", command=self.actualizar_producto, bg="#f39c12", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_producto, bg="#e74c3c", fg="white", width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario, bg="#95a5a6", fg="white", width=12).pack(side=tk.LEFT, padx=5)

        table_frame = tk.Frame(self.root, bg="#ecf0f1")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("ID", "Nombre", "Descripción", "Precio", "Cantidad", "Categoría", "Fecha")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "Descripción" else 180)

        self.tree.column("ID", width=50)
        self.tree.column("Precio", width=80)
        self.tree.column("Cantidad", width=80)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree.bind("<ButtonRelease-1>", self.seleccionar_producto)

    def load_productos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.controller.get_all_productos()
        for p in productos:
            self.tree.insert("", tk.END, values=p)

    def nuevo_producto(self):
        success, msg = self.controller.create_producto(
            self.entry_nombre.get(),
            self.entry_descripcion.get(),
            self.entry_precio.get(),
            self.entry_cantidad.get(),
            self.entry_categoria.get()
        )
        messagebox.showinfo("Resultado", msg)
        if success:
            self.load_productos()
            self.limpiar_formulario()

    def actualizar_producto(self):
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un producto para actualizar")
            return
        
        success, msg = self.controller.update_producto(
            self.producto_seleccionado,
            self.entry_nombre.get(),
            self.entry_descripcion.get(),
            self.entry_precio.get(),
            self.entry_cantidad.get(),
            self.entry_categoria.get()
        )
        messagebox.showinfo("Resultado", msg)
        if success:
            self.load_productos()
            self.limpiar_formulario()

    def eliminar_producto(self):
        if not self.producto_seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar")
            return
        
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?")
        if respuesta:
            success, msg = self.controller.delete_producto(self.producto_seleccionado)
            messagebox.showinfo("Resultado", msg)
            self.load_productos()
            self.limpiar_formulario()

    def buscar_productos(self):
        criterio = self.entry_buscar.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        productos = self.controller.search_productos(criterio)
        for p in productos:
            self.tree.insert("", tk.END, values=p)

    def seleccionar_producto(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item["values"]
            
            self.producto_seleccionado = valores[0]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, valores[1])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, valores[2])
            self.entry_precio.delete(0, tk.END)
            self.entry_precio.insert(0, valores[3])
            self.entry_cantidad.delete(0, tk.END)
            self.entry_cantidad.insert(0, valores[4])
            self.entry_categoria.delete(0, tk.END)
            self.entry_categoria.insert(0, valores[5])

    def limpiar_formulario(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.producto_seleccionado = None