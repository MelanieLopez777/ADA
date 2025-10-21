import tkinter as tk
from tkinter import ttk
import graphic


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Complejidad - Fibonacci")
        self.root.geometry("950x500")
        self.root.resizable(False, False)

        # --- Marco principal dividido ---
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # --- Frame para gráficas (izquierda) ---
        self.frame_graficas = ttk.Frame(self.main_frame, width=550)
        self.frame_graficas.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # --- Frame derecho para controles ---
        self.frame_controles = ttk.Frame(self.main_frame, width=350)
        self.frame_controles.pack(side="right", fill="y", padx=10, pady=10)

        # --- Instancia de la clase de gráficas ---
        self.grafica = graphic.Grafica(self.frame_graficas)

        # --- Controles UI ---
        ttk.Label(
            self.frame_controles,
            text="Análisis de Complejidad\nSerie de Fibonacci",
            font=("Segoe UI", 13, "bold"),
            justify="center"
        ).pack(pady=10)

        frame_input = ttk.Frame(self.frame_controles)
        frame_input.pack(pady=10)

        ttk.Label(frame_input, text="Valor máximo de n:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
        self.n_entry = ttk.Entry(frame_input, width=10)
        self.n_entry.insert(0, "30")
        self.n_entry.grid(row=0, column=1, padx=5)

        ttk.Button(self.frame_controles, text="Calcular Datos", command=self.calcular).pack(pady=10)
        ttk.Button(self.frame_controles, text="Gráfica de Tiempo", command=self.grafica.graphic_time).pack(pady=10)
        ttk.Button(self.frame_controles, text="Gráfica de Memoria", command=self.grafica.graphic_memory).pack(pady=10)

        self.status = ttk.Label(self.frame_controles, text="Listo", foreground="gray")
        self.status.pack(pady=10)

    def calcular(self):
        try:
            max_n = int(self.n_entry.get())
            if max_n < 5:
                self.status.config(text="⚠️ El valor debe ser ≥ 5", foreground="red")
                return
            self.status.config(text="Calculando...", foreground="blue")
            self.root.update()
            self.grafica.calculate_time_space(max_n=max_n)
            self.status.config(text=f"Datos calculados (n={max_n}) ✅", foreground="green")
        except ValueError:
            self.status.config(text="❌ Ingresa un número válido", foreground="red")
