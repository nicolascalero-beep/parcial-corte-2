import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import tkinter as tk
"""
DDD - Diseño Basado en el Dominio
=============================

Arquitectura por capas:
- dominio/       : Entidades, Value Objects, Services del dominio
- application/   : Casos de uso y lógica de aplicación
- infrastructure/ : Presentación (UI), Persistencia

Ejecutar: python parcial2_DDD/main.py
"""

def main():
    root = tk.Tk()
    from parcial2_DDD.infrastructure.views import ProductoView
    app = ProductoView(root)
    root.mainloop()

if __name__ == "__main__":
    main()