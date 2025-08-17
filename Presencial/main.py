import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Mi primera GUI")
root.geometry("500x500")

root.config(background="lightblue")

style = ttk.Style()
style.theme_use("clam")

lbl = tk.Label(root, text="¡Hola, GUI!", width=10, font=("Arial", 16, "bold"))
lbl.pack(pady=10)

lbl.config(fg="blue")


root.mainloop()