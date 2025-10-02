import itertools

class Graph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = {}

    def add_edge(self, vertex1, vertex2, weight = 0):
        if not vertex1 == vertex2:
            self.add_vertex(vertex1)
            self.add_vertex(vertex2)
            self.graph[vertex1][vertex2] = weight
            self.graph[vertex2][vertex1] = weight

    def display(self):
        for vertex, edges in self.graph.items():
            print(f"Vertice {vertex} se conecta con:")
            for neighbor, weight in edges.items():
                print(f"  - {neighbor} (peso: {weight})")

def problema_viajero(grafo: Graph, start: str):
    
    best_route = None
    best_cost = float("inf")
    vertex = list(grafo.graph.keys())
    
    if start in vertex:
        vertex.remove(start)

        for perm in itertools.permutations(vertex):
            route = [start] + list(perm) + [start] 
            cost = 0
            valid = True

            for i in range(len(route) - 1):
                v1, v2 = route[i], route[i + 1]
                if v2 in grafo.graph[v1]:
                    cost += grafo.graph[v1][v2]
                else:
                    valid = False
                    break
            
            print(f"\nPosibles camino: {route}, costo del camino: {cost}")

            if valid and cost < best_cost:
                best_cost = cost
                best_route = route
    else:
        best_route = None
        best_cost = None

    return best_route, best_cost


if __name__ == "__main__":
    grafo = Graph()
    grafo.add_edge("A", "B", 2)
    grafo.add_edge("A", "C", 5)
    grafo.add_edge("A", "D", 7)
    grafo.add_edge("B", "C", 8)
    grafo.add_edge("B", "D", 3)
    grafo.add_edge("D", "C", 1)

    grafo.display()
    route, cost = problema_viajero(grafo, "A")
    print("\nMejor camino:", route)
    print("Costo:", cost)
