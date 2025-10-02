import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import threading
from grafo import Grafo, coloracion_fuerza_bruta_con_visualizacion

# Colores de la paleta (NUEVA PALETA)
COLOR_FONDO = "#000000"        # Gris Claro
COLOR_PRIMARIO = "#113462"     # Azul Acero
COLOR_SECUNDARIO = "#f0f0f0"   # Gris Oscuro
COLOR_ACENTO = "#d2b99a"       # Naranja
COLOR_SECUNDARIO_2 = "#113462" # Salvia
COLOR_TEXTO = "#ffffff"        # Negro
COLOR_TEXTO_BOTON = "#f0f0f0"  # Blanco

# Configuración global de fuentes
FUENTE_TITULO = ("Arial", 16, "bold")
FUENTE_NORMAL = ("Arial", 14)
FUENTE_PEQUENA = ("Arial", 12)
FUENTE_BOTON = ("Arial", 14, "bold")

class GrafoColoreoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coloreo de Grafos - Algoritmo de Fuerza Bruta")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLOR_FONDO)
        
        self.configurar_estilos()
        
        self.grafo = Grafo()
        self.colores = ['#d62728', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        self.ejecutando = False
        self.delay = tk.DoubleVar(value=0.5)
        
        self.crear_interfaz()
        self.configurar_grafo_por_defecto()
    
    def configurar_estilos(self):
        estilo = ttk.Style()
        #estilo.theme_use('clam')
        
        estilo.configure("TFrame", background=COLOR_FONDO)
        estilo.configure("TLabel", font=FUENTE_NORMAL, background=COLOR_FONDO, foreground=COLOR_TEXTO)
        estilo.configure("TButton", font=FUENTE_BOTON, padding=(10, 5), 
                        background=COLOR_PRIMARIO, foreground=COLOR_TEXTO_BOTON)
        estilo.configure("TEntry", font=FUENTE_NORMAL)
        estilo.configure("TScale", troughcolor=COLOR_SECUNDARIO_2)
        
        estilo.map("TButton",
                  background=[('active', COLOR_ACENTO), ('pressed', COLOR_SECUNDARIO_2)],
                  foreground=[('active', COLOR_TEXTO_BOTON), ('pressed', COLOR_TEXTO_BOTON)])
        
    def crear_interfaz(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        control_frame = ttk.Frame(main_frame, padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        for i in range(5):
            control_frame.columnconfigure(i, weight=1)
        
        ttk.Button(control_frame, text="Iniciar coloreo", command=self.iniciar_coloreo).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        ttk.Button(control_frame, text="Pausa/Reanudar", command=self.pausar_reanudar).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ttk.Button(control_frame, text="Reiniciar", command=self.reiniciar).grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        
        ttk.Label(control_frame, text="Velocidad:", font=FUENTE_NORMAL).grid(row=0, column=3, padx=(15, 0), pady=5, sticky="e")
        ttk.Scale(control_frame, from_=0.1, to=2.0, variable=self.delay, orient=tk.HORIZONTAL, length=150).grid(row=0, column=4, padx=(0, 10), pady=5, sticky="w")
        
        info_frame = ttk.Frame(main_frame, padding="10")
        info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        self.info_text = tk.Text(info_frame, width=35, height=20, font=FUENTE_PEQUENA, 
                                wrap=tk.WORD, bg=COLOR_TEXTO_BOTON, fg="#000000", 
                                bd=2, insertbackground=COLOR_TEXTO_BOTON)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.info_text.configure(yscrollcommand=scrollbar.set)
        
        graph_frame = ttk.Frame(main_frame, padding="10")
        graph_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        graph_frame.columnconfigure(0, weight=1)
        graph_frame.rowconfigure(0, weight=1)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.patch.set_facecolor(COLOR_FONDO)
        self.ax.set_facecolor(COLOR_FONDO)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        edit_frame = ttk.Frame(main_frame, padding="10")
        edit_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))
        
        ttk.Label(edit_frame, text="Vértice:", font=FUENTE_NORMAL).grid(row=0, column=0, padx=5, pady=5)
        self.vertice_entry = ttk.Entry(edit_frame, width=15, font=FUENTE_NORMAL)
        self.vertice_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(edit_frame, text="Agregar", command=self.agregar_vertice).grid(row=0, column=2, padx=10, pady=5)
        
        ttk.Label(edit_frame, text="Arista:", font=FUENTE_NORMAL).grid(row=0, column=3, padx=5, pady=5)
        self.arista_origen_entry = ttk.Entry(edit_frame, width=8, font=FUENTE_NORMAL)
        self.arista_origen_entry.grid(row=0, column=4, padx=5, pady=5)
        ttk.Label(edit_frame, text="-", font=FUENTE_NORMAL).grid(row=0, column=5, padx=2, pady=5)
        self.arista_destino_entry = ttk.Entry(edit_frame, width=8, font=FUENTE_NORMAL)
        self.arista_destino_entry.grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(edit_frame, text="Agregar", command=self.agregar_arista).grid(row=0, column=7, padx=10, pady=5)
        
        ttk.Button(edit_frame, text="Grafo por defecto", command=self.configurar_grafo_por_defecto).grid(row=0, column=8, padx=20, pady=5)
        
    def configurar_grafo_por_defecto(self):
        self.grafo = Grafo()
        self.grafo.agregar_arista('a','b')
        self.grafo.agregar_arista('a','c')
        self.grafo.agregar_arista('a','d')
        self.grafo.agregar_arista('b','c')
        self.grafo.agregar_arista('c','d')
        
        self.actualizar_visualizacion()
        self.agregar_info("Grafo por defecto cargado.")
        
    def agregar_vertice(self):
        vertice = self.vertice_entry.get().strip()
        if vertice:
            self.grafo.agregar_vertice(vertice)
            self.actualizar_visualizacion()
            self.agregar_info(f"Vértice '{vertice}' agregado.")
            self.vertice_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un nombre para el vértice.")
    
    def agregar_arista(self):
        origen = self.arista_origen_entry.get().strip()
        destino = self.arista_destino_entry.get().strip()
        
        if origen and destino:
            self.grafo.agregar_arista(origen, destino)
            self.actualizar_visualizacion()
            self.agregar_info(f"Arista '{origen}-{destino}' agregada.")
            self.arista_origen_entry.delete(0, tk.END)
            self.arista_destino_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese ambos vértices para la arista.")
    
    def agregar_info(self, mensaje):
        self.info_text.insert(tk.END, f"{mensaje}\n")
        self.info_text.see(tk.END)
        self.info_text.update_idletasks()
    
    def actualizar_visualizacion(self, asignacion=None, k=0, estado=""):
        self.ax.clear()
        self.ax.set_facecolor(COLOR_FONDO)
        
        G = nx.Graph()
        G.add_nodes_from(self.grafo.lista_vertices())
        
        for u in self.grafo.lista_vertices():
            v_obj = self.grafo.obtener_vertice(u)
            for v_conn in v_obj.obtener_conexiones():
                G.add_edge(u, v_conn.valor)
        
        pos = nx.spring_layout(G)
        
        node_colors = COLOR_SECUNDARIO_2
        if asignacion:
            node_colors = [self.colores[asignacion[nodo] % len(self.colores)] for nodo in G.nodes()]
            title = f"{estado}"
        else:
            title = ""
            
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=800, ax=self.ax)
        nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', ax=self.ax, font_color=COLOR_TEXTO)
        nx.draw_networkx_edges(G, pos, width=2, ax=self.ax, edge_color=COLOR_SECUNDARIO)
        
        self.ax.set_title(title, fontsize=16, fontweight='bold', color=COLOR_TEXTO)
        self.ax.axis('off')
        self.canvas.draw()
    
    def actualizar_ui_callback(self, asignacion, k, estado):
        if not self.ejecutando:
            return False
        
        self.actualizar_visualizacion(asignacion, k, estado)
        self.agregar_info(estado)
        return True
    
    def iniciar_coloreo(self):
        if self.ejecutando:
            return
        
        if len(self.grafo.lista_vertices()) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío. Agregue vértices y aristas.")
            return
        
        self.ejecutando = True
        self.agregar_info("Iniciando algoritmo de coloreo...")
        
        thread = threading.Thread(target=self.ejecutar_algoritmo)
        thread.daemon = True
        thread.start()
    
    def ejecutar_algoritmo(self):
        try:
            k_min, asignacion = coloracion_fuerza_bruta_con_visualizacion(
                self.grafo, 
                self.actualizar_ui_callback,
                self.delay.get()
            )
            
            if k_min != -1: # Si no fue detenido
                self.agregar_info(f"Algoritmo completado. Número cromático: {k_min}")
        except Exception as e:
            self.agregar_info(f"Error durante la ejecución: {str(e)}")
        finally:
            self.ejecutando = False
    
    def pausar_reanudar(self):
        self.ejecutando = not self.ejecutando
        estado = "reanudado" if self.ejecutando else "pausado"
        self.agregar_info(f"Algoritmo {estado}.")
    
    def reiniciar(self):
        self.ejecutando = False
        self.info_text.delete(1.0, tk.END)
        self.configurar_grafo_por_defecto()
        self.agregar_info("Visualización reiniciada.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GrafoColoreoGUI(root)
    root.mainloop(1)