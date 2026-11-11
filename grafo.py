"""TDA Grafo no dirigido y ponderado, con los algoritmos usados en los ejercicios."""
from collections import deque
import heapq


class Grafo:
    def __init__(self, dirigido=False):
        self.dirigido = dirigido
        self.vertices = {}      # nombre -> datos extra (ej: {"tipo": "pc"})
        self.adyacentes = {}    # nombre -> {vecino: peso}

    # ---------------- carga ----------------
    def insertar_vertice(self, nombre, **datos):
        self.vertices[nombre] = datos
        self.adyacentes.setdefault(nombre, {})

    def insertar_arista(self, origen, destino, peso):
        self.adyacentes[origen][destino] = peso
        if not self.dirigido:
            self.adyacentes[destino][origen] = peso

    def eliminar_arista(self, origen, destino):
        self.adyacentes[origen].pop(destino, None)
        if not self.dirigido:
            self.adyacentes[destino].pop(origen, None)

    def tipo(self, nombre):
        return self.vertices[nombre].get("tipo")

    def vecinos(self, nombre):
        # orden alfabético para que los barridos sean deterministas
        return sorted(self.adyacentes[nombre])

    # ---------------- barridos ----------------
    def barrido_profundidad(self, inicio):
        visitados, resultado = set(), []

        def dfs(v):
            visitados.add(v)
            resultado.append(v)
            for w in self.vecinos(v):
                if w not in visitados:
                    dfs(w)

        dfs(inicio)
        return resultado

    def barrido_amplitud(self, inicio):
        visitados, resultado = {inicio}, []
        cola = deque([inicio])
        while cola:
            v = cola.popleft()
            resultado.append(v)
            for w in self.vecinos(v):
                if w not in visitados:
                    visitados.add(w)
                    cola.append(w)
        return resultado

    # ---------------- caminos ----------------
    def dijkstra(self, origen):
        """Devuelve (distancias, previos) desde origen a todos los vértices."""
        distancias = {v: float("inf") for v in self.vertices}
        previos = {v: None for v in self.vertices}
        distancias[origen] = 0
        heap = [(0, origen)]
        while heap:
            d, v = heapq.heappop(heap)
            if d > distancias[v]:
                continue
            for w, peso in self.adyacentes[v].items():
                nueva = d + peso
                if nueva < distancias[w]:
                    distancias[w] = nueva
                    previos[w] = v
                    heapq.heappush(heap, (nueva, w))
        return distancias, previos

    def camino_mas_corto(self, origen, destino):
        """Devuelve (lista_de_vertices, costo_total)."""
        distancias, previos = self.dijkstra(origen)
        if distancias[destino] == float("inf"):
            return None, float("inf")
        camino, actual = [], destino
        while actual is not None:
            camino.append(actual)
            actual = previos[actual]
        return camino[::-1], distancias[destino]

    # ---------------- árbol de expansión mínima ----------------
    def kruskal(self):
        """Devuelve (lista de aristas (u, v, peso), peso_total)."""
        padre = {v: v for v in self.vertices}

        def buscar(v):
            while padre[v] != v:
                padre[v] = padre[padre[v]]
                v = padre[v]
            return v

        aristas = sorted(
            {(p, *sorted((u, v))) for u in self.adyacentes
             for v, p in self.adyacentes[u].items()}
        )
        arbol, total = [], 0
        for peso, u, v in aristas:
            ru, rv = buscar(u), buscar(v)
            if ru != rv:
                padre[ru] = rv
                arbol.append((u, v, peso))
                total += peso
        return arbol, total
