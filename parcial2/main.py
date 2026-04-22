import tkinter as tk
from view import View

def main():
    root = tk.Tk()
    app = View(root)
    root.mainloop()

if __name__ == "__main__":
    main()