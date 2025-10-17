import tkinter as tk
from tkinter import ttk
import graphic  


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Complejidad - Fibonacci")
        self.root.geometry("420x350")
        self.root.resizable(False, False)

        # Instancia del graficador
        self.grafica = graphic.Grafica()

        # --- Título ---
        ttk.Label(
            root,
            text="Análisis de Complejidad - Serie de Fibonacci",
            font=("Segoe UI", 13, "bold")
        ).pack(pady=10)

        # --- Entrada de max_n ---
        frame_input = ttk.Frame(root)
        frame_input.pack(pady=10)

        ttk.Label(frame_input, text="Valor máximo de n:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
        self.n_entry = ttk.Entry(frame_input, width=10)
        self.n_entry.insert(0, "30")  # valor por defecto
        self.n_entry.grid(row=0, column=1, padx=5)

        # --- Botones ---
        ttk.Button(root, text="Calcular y Graficar Datos", command=self.calcular).pack(pady=8)
        ttk.Button(root, text="Mostrar Gráfica de Tiempo", command=self.grafica.graphic_time).pack(pady=8)
        ttk.Button(root, text="Mostrar Gráfica de Memoria", command=self.grafica.graphic_memory).pack(pady=8)

        # --- Estado ---
        self.status = ttk.Label(root, text="Listo", foreground="gray")
        self.status.pack(pady=10)

    def calcular(self):
        """Ejecuta los cálculos según el valor ingresado de n."""
        try:
            # Obtener valor ingresado por el usuario
            max_n = int(self.n_entry.get())

            if max_n < 5:
                self.status.config(text="⚠️ El valor debe ser mayor o igual a 5", foreground="red")
                return

            self.status.config(text="Calculando...", foreground="blue")
            self.root.update()

            # Ejecutar los cálculos con el valor de max_n
            self.grafica.calculate_time_space(max_n=max_n)

            self.status.config(text=f"Datos calculados correctamente (hasta n={max_n}) ✅", foreground="green")

        except ValueError:
            self.status.config(text="❌ Ingresa un número válido para n", foreground="red")
