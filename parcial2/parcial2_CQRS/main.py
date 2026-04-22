import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import tkinter as tk
"""
CQRS - Command Query Responsibility Segregation
===========================================

Arquitectura CQRS:
- commands/    : Intentos de cambio (escritura)
- queries/    : Consultas de datos (lectura)
- handlers/   : Manejadores de commands y queries
- infrastructure/ : Presentación y base de datos

Ejecutar: python parcial2_CQRS/main.py
"""

def main():
    root = tk.Tk()
    from parcial2_CQRS.infrastructure.views import ProductoView
    app = ProductoView(root)
    root.mainloop()

if __name__ == "__main__":
    main()