import fibonacci
import time
import matplotlib.pyplot as plt
from memory_profiler import memory_usage
import numpy as np

import tkinter as tk


class Grafica:

    def __init__(self):
        
        self.values = []
        self.time_dp = []
        self.memory_dp = []
        self.time_r = []
        self.memory_r = []

    # En graphic.py

    def calculate_time_space(self, max_n=30):
        """
        Calcula el tiempo de ejecución y el uso de memoria para las
        funciones de Fibonacci y almacena los resultados.
        """
        # 1. Limpiar las listas antes de cada cálculo
        self.values.clear()
        self.time_dp.clear()
        self.memory_dp.clear()
        self.time_r.clear()
        self.memory_r.clear()

        print(f"Iniciando cálculos hasta n={max_n}...")

        # 2. Iterar para cada valor de n
        for n in range(5, max_n + 1, 5):
            # Almacena el valor de 'n' para el eje X
            self.values.append(n)

            # --- Medición de TIEMPO para DP ---
            start_time_dp = time.perf_counter()
            fibonacci.fibonacci_dp(n)
            end_time_dp = time.perf_counter()
            self.time_dp.append(end_time_dp - start_time_dp)

            # --- Medición de TIEMPO para Recursiva ---
            start_time_r = time.perf_counter()
            fibonacci.fibonacci_r(n)
            end_time_r = time.perf_counter()
            self.time_r.append(end_time_r - start_time_r) 

            # --- Medición de MEMORIA ---
            mem_dp = memory_usage((fibonacci.fibonacci_dp, (n,)), max_iterations=1, interval=0.1)
            self.memory_dp.append(np.mean(mem_dp))
            
            mem_r = memory_usage((fibonacci.fibonacci_r, (n,)), max_iterations=1, interval=0.1)
            self.memory_r.append(np.mean(mem_r))
            
            print(f"Calculado para n={n}...")

        # 3. El bloque redundante de "Almacenar valores" se ha ELIMINADO.
        
        print("✅ Cálculos finalizados. ¡Ya puedes graficar!")
            

    def graphic_time(self):
        """Grafica la complejidad temporal."""
        if not self.values:
            print("No hay datos para graficar. Por favor, ejecuta los cálculos primero.")
            return
    
        plt.figure(figsize=(8, 5))
        plt.plot(self.values, self.time_dp, 'o-r', label="DP (Dinámica)")
        plt.plot(self.values, self.time_r, 'o-b', label="Recursiva")
        plt.title("Complejidad Temporal")
        plt.xlabel("n")
        plt.ylabel("Tiempo (segundos)")
        plt.legend()
        plt.grid(True)
        plt.show()

    def graphic_memory(self):
        
        if not self.values:
            print("No hay datos para graficar. Por favor, ejecuta los cálculos primero.")
            return

        """Grafica la complejidad espacial (promedio de memoria)."""
        plt.figure(figsize=(8, 5))
        plt.plot(self.values, self.memory_dp, 'o-g', label="DP (Dinámica)")
        plt.plot(self.values, self.memory_r, 'o-m', label="Recursiva")
        plt.title("Complejidad Espacial (Promedio de Memoria - memory_profiler)")
        plt.xlabel("n")
        plt.ylabel("Memoria utilizada promedio (MiB)")
        plt.legend()
        plt.grid(True)
        plt.show()







