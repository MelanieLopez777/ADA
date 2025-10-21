import fibonacci
import time
import numpy as np
from memory_profiler import memory_usage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from utils.color_palette import ColorPalette


class Grafica:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame  
        self.values = []
        self.time_dp = []
        self.memory_dp = []
        self.time_r = []
        self.memory_r = []

        self.canvas = None

        self.color_dp_time = ColorPalette.get_hex("Denim Blue")
        self.color_r_time = ColorPalette.get_hex("Azalea Pink")
        self.color_dp_mem = ColorPalette.get_hex("Spring Green")
        self.color_r_mem = ColorPalette.get_hex("Blush Pink")

    def clear_plot(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

    def calculate_time_space(self, max_n=30):

        import matplotlib.pyplot as plt 
        
        self.values.clear()
        self.time_dp.clear()
        self.memory_dp.clear()
        self.time_r.clear()
        self.memory_r.clear()

        print(f"Iniciando cálculos hasta n={max_n}...")

        for n in range(5, max_n + 1, 5):
            self.values.append(n)

            start_time_dp = time.perf_counter()
            fibonacci.fibonacci_dp(n)
            end_time_dp = time.perf_counter()
            self.time_dp.append(end_time_dp - start_time_dp)

            start_time_r = time.perf_counter()
            fibonacci.fibonacci_r(n)
            end_time_r = time.perf_counter()
            self.time_r.append(end_time_r - start_time_r) 

            mem_dp = memory_usage((fibonacci.fibonacci_dp, (n,)), max_iterations=1, interval=0.1)
            self.memory_dp.append(np.mean(mem_dp))
            
            mem_r = memory_usage((fibonacci.fibonacci_r, (n,)), max_iterations=1, interval=0.1)
            self.memory_r.append(np.mean(mem_r))
            
            print(f"Calculado para n={n}...")
            

    def _plot(self, x, y1, y2, label1, label2, title, ylabel, color1, color2):
        self.clear_plot()

        fig = Figure(figsize=(5.5, 4.2), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(x, y1, 'o-', color=color1, label=label1)
        ax.plot(x, y2, 'o-', color=color2, label=label2)
        ax.set_title(title)
        ax.set_xlabel("n")
        ax.set_ylabel(ylabel)
        ax.legend()
        ax.grid(True)

        self.canvas = FigureCanvasTkAgg(fig, master=self.parent_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def graphic_time(self):
        if not self.values:
            print("No hay datos para graficar.")
            return
        self._plot(
            self.values,
            self.time_dp,
            self.time_r,
            "DP (Dinámica)",
            "Recursiva",
            "Complejidad Temporal",
            "Tiempo (segundos)",
            self.color_dp_time,
            self.color_r_time
        )

    def graphic_memory(self):
        if not self.values:
            print("No hay datos para graficar.")
            return
        self._plot(
            self.values,
            self.memory_dp,
            self.memory_r,
            "DP (Dinámica)",
            "Recursiva",
            "Complejidad Espacial",
            "Memoria promedio (MiB)",
            self.color_dp_mem,
            self.color_r_mem
        )