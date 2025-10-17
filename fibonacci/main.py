import tkinter as tk
from tkinter import messagebox
from gui import App

def main():
    try:
        root = tk.Tk()
        root.title("Análisis de Complejidad - Serie de Fibonacci")
        app = App(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
