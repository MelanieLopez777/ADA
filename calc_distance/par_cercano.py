import tkinter as tk
from tkinter import messagebox, ttk
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


RANGO = 40
puntos = []

def distancia(i, j) -> float:
    return math.sqrt(
        (puntos[i][0] - puntos[j][0]) ** 2 +
        (puntos[i][1] - puntos[j][1]) ** 2
    )

def distancia_menor():
    if len(puntos) < 2:
        return None, None, float(RANGO)
    
    min_distancia = float(RANGO)
    par_minimo = (None, None)

    for i in range(len(puntos)):
        for j in range(i + 1, len(puntos)):
            d = distancia(i, j)
            print(f"Distancia entre punto {i} y punto {j} = {d:.2f}")

            if d < min_distancia:
                min_distancia = d
                par_minimo = (i, j)

    print(f"\nLa menor distancia es {min_distancia:.2f} entre los puntos {par_minimo[0]} y {par_minimo[1]}: {puntos[par_minimo[0]]} y {puntos[par_minimo[1]]}")
    
    return par_minimo[0], par_minimo[1], min_distancia

# Manejo de gráfica

def actualizar_grafica(canvas, fig, ax, punto1_idx=None, punto2_idx=None):
    ax.clear()
    
    if len(puntos) > 0:
        x_vals = [p[0] for p in puntos]
        y_vals = [p[1] for p in puntos]
        
        ax.scatter(x_vals, y_vals, color="#e665bd", s=50, label='Puntos')
        
        if punto1_idx is not None and punto2_idx is not None:
            ax.scatter([puntos[punto1_idx][0], puntos[punto2_idx][0]], 
                      [puntos[punto1_idx][1], puntos[punto2_idx][1]], 
                      color="#8e54c4", s=100, label='Puntos más cercanos')
            
            ax.plot([puntos[punto1_idx][0], puntos[punto2_idx][0]], 
                   [puntos[punto1_idx][1], puntos[punto2_idx][1]], 
                   color="#6409b8", linestyle='--', alpha=0.5)
        
        ax.set_xlabel('Coordenada X')
        ax.set_ylabel('Coordenada Y')
        ax.set_title('Distribución de Puntos')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
    
    canvas.draw()

# Aplicación
root = tk.Tk()
root.title("Visualizador de pares más cercanos entre puntos")
root.geometry("1200x800")  

# Frame principal que divide izquierda y derecha
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Frame izquierdo para la gráfica
left_frame = tk.Frame(main_frame, width=500, bg="#f0f0f0")
left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
left_frame.pack_propagate(False)

# Título de la sección de gráfica
tk.Label(left_frame, text="Gráfica de Puntos", bg="#f0f0f0", font=("Arial", 12, "bold")).pack(pady=(0, 10))

# Crear figura de matplotlib
fig = plt.Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)

# Crear canvas para la gráfica
canvas_grafica = FigureCanvasTkAgg(fig, left_frame)
canvas_grafica.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

ax.set_xlabel('Coordenada X')
ax.set_ylabel('Coordenada Y')
ax.set_title('Distribución de Puntos')
ax.grid(True, linestyle='--', alpha=0.7)
canvas_grafica.draw()

# Frame  para ingresar puntos y mostrar resultados

right_frame = tk.Frame(main_frame, width=400, bg="#e0e0e0")
right_frame.pack(side="right", fill="both", padx=(10, 0))
right_frame.pack_propagate(False)

# Título de la sección de puntos

title_frame = tk.Frame(right_frame, bg="#e0e0e0")
title_frame.pack(fill="x", pady=(0, 10))
tk.Label(title_frame, text="Ingreso de Puntos", bg="#e0e0e0", font=("Arial", 12, "bold")).pack()

# Frame para los encabezados de la tabla

header_frame = tk.Frame(right_frame, bg="#b384b8")
header_frame.pack(fill="x", pady=(0, 5))

# Encabezados de la tabla 

tk.Label(header_frame, text="Puntos", width=10, bg="#b384b8", font=("Arial", 10, "bold")).pack(side="left", padx=(10, 0))
tk.Label(header_frame, text=" Valores de x", width=12, bg="#b384b8", font=("Arial", 10, "bold")).pack(side="left", padx=20)
tk.Label(header_frame, text="Valores de y", width=12, bg="#b384b8", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 10))

# Frames para scrollbar

container = tk.Frame(right_frame, height=200)
container.pack(fill="x", pady=(0, 10))

canvas = tk.Canvas(container, height=200)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Listas para almacenar las entradas
x_entries = []
y_entries = []

# Crear 5 filas para puntos

for i in range(5):
    row_frame = tk.Frame(scrollable_frame)
    row_frame.pack(fill="x", pady=2)
    
    # Etiqueta del punto

    tk.Label(row_frame, text=f"p{i+1}", width=14, bg="#e6e6e6", relief="solid").pack(side="left", padx=(10, 0))
    
    # Entrada para x
    x_entry = tk.Entry(row_frame, width=14, justify="center", relief="solid")
    x_entry.pack(side="left", padx=20)
    x_entries.append(x_entry)
    
    # Entrada para y
    y_entry = tk.Entry(row_frame, width=14, justify="center", relief="solid")
    y_entry.pack(side="left", padx=(0, 10))
    y_entries.append(y_entry)

canvas.pack(side="left", fill="x", expand=True)
scrollbar.pack(side="right", fill="y")

# Frame para botones (más ancho)
button_frame = tk.Frame(right_frame, bg="#e0e0e0", height=50)
button_frame.pack(fill="x", pady=(0, 15))
button_frame.pack_propagate(False)

# Función para llenado automático
def auto_fill():
    for x_entry, y_entry in zip(x_entries, y_entries):
        if not x_entry.get() and not y_entry.get():
            x_entry.insert(0, str(round(random.uniform(0, 100), 2)))
            y_entry.insert(0, str(round(random.uniform(0, 100), 2)))

# Función para limpiar campos
def clear_fields():
    for x_entry in x_entries:
        x_entry.delete(0, tk.END)
    for y_entry in y_entries:
        y_entry.delete(0, tk.END)

# Función para procesar datos
def process_data():
    global puntos
    puntos = []  # Reiniciar la lista de puntos
    
    for i, (x_entry, y_entry) in enumerate(zip(x_entries, y_entries)):
        x_val = x_entry.get()
        y_val = y_entry.get()
        
        if x_val and y_val:
            try:
                x = float(x_val)
                y = float(y_val)
                puntos.append((x, y))
            except ValueError:
                messagebox.showerror("Error", f"Valores inválidos en punto p{i+1}")
                return
        elif x_val or y_val:
            messagebox.showerror("Error", f"Falta un valor en punto p{i+1}")
            return
    
    if len(puntos) < 2:
        messagebox.showerror("Error", "Se necesitan al menos 2 puntos")
        return
    
    # Calcular la distancia menor
    punto1_idx, punto2_idx, min_distancia = distancia_menor()
    
    # Actualizar el área de resultados
    result_text.config(state="normal")
    result_text.delete("1.0", tk.END)
    
    if punto1_idx is not None and punto2_idx is not None:
        result_text.insert("1.0", f"Puntos ingresados: {len(puntos)}\n\n")
        result_text.insert(tk.END, f"Par de puntos más cercanos:\n")
        result_text.insert(tk.END, f"Punto {punto1_idx+1}: {puntos[punto1_idx]}\n")
        result_text.insert(tk.END, f"Punto {punto2_idx+1}: {puntos[punto2_idx]}\n")
        result_text.insert(tk.END, f"Distancia: {min_distancia:.4f}\n\n")
        
        result_text.insert(tk.END, "Todos los puntos:\n")
        for i, punto in enumerate(puntos):
            result_text.insert(tk.END, f"Punto {i+1}: {punto}\n")
    else:
        result_text.insert("1.0", "No hay suficientes puntos para calcular distancias.")
    
    result_text.config(state="disabled")
    
    actualizar_grafica(canvas_grafica, fig, ax, punto1_idx, punto2_idx)

# Botones de acción

button_container = tk.Frame(button_frame, bg="#e0e0e0")
button_container.pack(fill="both", expand=True, padx=10, pady=5)

tk.Button(button_container, text="Llenado automático", command=auto_fill, bg="#d4b9d8", 
          relief="raised", width=15).pack(side="left", padx=(0, 10))
tk.Button(button_container, text="Limpiar campos", command=clear_fields, bg="#d277e0", 
          relief="raised", width=15).pack(side="left", padx=(0, 10))
tk.Button(button_container, text="Procesar datos", command=process_data, bg="#985fdf", 
          relief="raised", width=15).pack(side="right")


# Área para mostrar resultados 

result_frame = tk.Frame(right_frame, bg="#e0e0e0")
result_frame.pack(fill="both", expand=True)

tk.Label(result_frame, text="Resultados", bg="#e0e0e0", font=("Arial", 12, "bold")).pack(pady=(0, 5))

# Área para mostrar resultados

result_text = tk.Text(result_frame, height=15, wrap="word", bg="white", relief="sunken", bd=2)
result_text.pack(fill="both", expand=True, padx=10, pady=5)
result_text.insert("1.0", "Los resultados se mostrarán aquí después de procesar los datos.")
result_text.config(state="disabled")

root.mainloop()