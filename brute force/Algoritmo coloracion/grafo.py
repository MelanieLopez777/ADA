import time
from itertools import product

class Vertice():
    def __init__(self, valor):
        self.valor = valor
        self.conexiones = {}
        
    def agregar_conexion(self, vertice, peso=0):
        self.conexiones[vertice] = peso
        
    def obtener_conexiones(self):
        return list(self.conexiones.keys())
        
    def obtener_peso(self, vertice):
        return self.conexiones.get(vertice)
        
    def __repr__(self):
        return f"Vertice({self.valor})"
        
class Grafo():
    def __init__(self):
        self.vertices = {}
        
    def agregar_vertice(self, valor):
        if valor not in self.vertices:
            nuevoVertice = Vertice(valor)
            self.vertices[valor] = nuevoVertice
            return nuevoVertice
        return self.vertices[valor]
        
    def agregar_arista(self, origen, destino, peso=0):
        if origen not in self.vertices:
            self.agregar_vertice(origen)
            
        if destino not in self.vertices:
            self.agregar_vertice(destino)
        
        self.vertices[origen].agregar_conexion(self.vertices[destino], peso)
        self.vertices[destino].agregar_conexion(self.vertices[origen], peso)
        #return
    
    def obtener_peso(self, origen, destino):
        v_origen = self.vertices.get(origen)
        v_destino = self.vertices.get(destino)
        if not v_origen or not v_destino:
            return None
        return v_origen.obtener_peso(v_destino)

    def obtener_vertice(self, vertice):
        return self.vertices.get(vertice)
        
    def tiene_arista(self, origen, destino):
        v_origen = self.vertices.get(origen)
        v_destino = self.vertices.get(destino)
        if not v_origen or not v_destino:
            return False
        return v_destino in v_origen.conexiones

    def __iter__(self):
        return iter(self.vertices.values())

    def lista_vertices(self):
        return list(self.vertices.keys())

# ---------------------------------------------------------
#                   Algoritmo de coloración 
# ----------------------------------------------------------

def es_coloreo_valido(grafo, asignacion):
    
    """ 
    u -> toma el valor de un vértice por cada iteración de todos
    los vertices contenidos en el grafo 
    
    v_obj -> toma el valor de cada una de las conexiones del 
    vértice definido en u por cada iteración 
    """
    for u in grafo.lista_vertices():
        for v_obj in grafo.obtener_vertice(u).obtener_conexiones():
            v = v_obj.valor
            if u not in asignacion or v not in asignacion:
                return False
            if asignacion[u] == asignacion[v]:
                return False
    return True

def coloracion_fuerza_bruta_con_visualizacion(grafo, actualizar_ui_callback=None, delay=0.5):

    vertices = grafo.lista_vertices()
    n = len(vertices)

    # Si no hay vértices entonces no hay coloración
    if n == 0:
        return 0, {}

    """
    k -> variable asignada para representar el número cromático, varia 
    según el número de vértices

    tuplas_colores -> es el resultado de aplicar el producto cartesiano
    para encontrar todas las posibles combinaciones entre colores y vértices
    según k

    asignacion ->  define el color correspondiente a cada vertice
    """
    for k in range(1, n+1):
        for tupla_colores in product(range(k), repeat=n):
            asignacion = {vertices[i]: tupla_colores[i] for i in range(n)}
            
            if actualizar_ui_callback:
                actualizar_ui_callback(asignacion, k, f"Probando con {k} colores")
            
            time.sleep(delay)
            
            if es_coloreo_valido(grafo, asignacion):
                if actualizar_ui_callback:
                    actualizar_ui_callback(asignacion, k, f"¡Solución encontrada! Número cromático: {k}")
                return k, asignacion
    
    """
    En caso de no encontrarse coloraciones válidas 
    se asigna un color a cada vértice
    """
    asignacion_final = {v: i for i, v in enumerate(vertices)}
    if actualizar_ui_callback:
        actualizar_ui_callback(asignacion_final, n, f"Solución trivial. Número cromático: {n}")
    return n, asignacion_final