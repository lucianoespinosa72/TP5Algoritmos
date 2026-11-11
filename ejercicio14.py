"""Ejercicio 14 - Ambientes de una casa en un grafo NO dirigido.

Pesos = distancia en metros entre ambientes.
Todos los vértices tienen al menos 3 aristas; Cocina y Comedor tienen 5.
"""
from grafo import Grafo

# a. vértices = ambientes de la casa
AMBIENTES = [
    "Cocina", "Comedor", "Cochera", "Quincho", "Baño 1", "Baño 2",
    "Habitación 1", "Habitación 2", "Sala de estar", "Terraza", "Patio",
]

# b. aristas con distancias en metros
ARISTAS = [
    # Cocina (5 aristas)
    ("Cocina", "Comedor", 4),
    ("Cocina", "Quincho", 9),
    ("Cocina", "Patio", 7),
    ("Cocina", "Baño 1", 6),
    ("Cocina", "Sala de estar", 5),
    # Comedor (5 aristas, contando Cocina)
    ("Comedor", "Sala de estar", 3),
    ("Comedor", "Terraza", 10),
    ("Comedor", "Habitación 1", 8),
    ("Comedor", "Baño 2", 7),
    # Resto
    ("Cochera", "Patio", 6),
    ("Cochera", "Quincho", 12),
    ("Cochera", "Baño 1", 11),
    ("Quincho", "Patio", 4),
    ("Baño 1", "Habitación 2", 5),
    ("Baño 2", "Habitación 1", 3),
    ("Baño 2", "Habitación 2", 4),
    ("Habitación 1", "Habitación 2", 6),
    ("Sala de estar", "Terraza", 6),
    ("Terraza", "Patio", 9),
]


def cargar_casa():
    g = Grafo(dirigido=False)
    for amb in AMBIENTES:
        g.insertar_vertice(amb)
    for u, v, m in ARISTAS:
        g.insertar_arista(u, v, m)
    return g


def titulo(texto):
    print(f"\n{'=' * 60}\n{texto}\n{'=' * 60}")


def main():
    g = cargar_casa()

    titulo("a/b. Ambientes y cantidad de conexiones")
    for amb in AMBIENTES:
        conexiones = ", ".join(f"{v} ({m} m)" for v, m in g.adyacentes[amb].items())
        print(f"  {amb:13} [{len(g.adyacentes[amb])}]: {conexiones}")

    titulo("c. Árbol de expansión mínima (Kruskal)")
    arbol, total = g.kruskal()
    for u, v, m in arbol:
        print(f"  {u} - {v}: {m} m")
    print(f"  => Se necesitan {total} metros de cable para conectar todos los ambientes")

    titulo("d. Camino más corto Habitación 1 -> Sala de estar")
    camino, metros = g.camino_mas_corto("Habitación 1", "Sala de estar")
    print(f"  Camino: {' -> '.join(camino)}")
    print(f"  => Se necesitan {metros} metros de cable de red (router -> Smart TV)")


if __name__ == "__main__":
    main()
