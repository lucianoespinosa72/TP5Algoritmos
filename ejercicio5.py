"""Ejercicio 5 - Esquema de red cargado en un grafo NO dirigido (punto h).

Aristas, pesos y tipos cargados según la figura del enunciado
(16 equipos, 16 conexiones; el único ciclo es Router 1 - Router 2 - Router 3).
"""
from grafo import Grafo

# a. cada nodo almacena nombre y tipo
EQUIPOS = {
    "Debian": "notebook",
    "Red Hat": "notebook",
    "Arch": "notebook",
    "Ubuntu": "pc",
    "Mint": "pc",
    "Manjaro": "pc",
    "Parrot": "pc",
    "Fedora": "pc",
    "Guaraní": "servidor",
    "MongoDB": "servidor",
    "Router 1": "router",
    "Router 2": "router",
    "Router 3": "router",
    "Switch 1": "switch",
    "Switch 2": "switch",
    "Impresora": "impresora",
}

ARISTAS = [
    ("Switch 1", "Debian", 17),
    ("Switch 1", "Ubuntu", 18),
    ("Switch 1", "Mint", 80),
    ("Switch 1", "Impresora", 22),
    ("Switch 1", "Router 1", 29),
    ("Router 1", "Router 2", 37),
    ("Router 1", "Router 3", 43),
    ("Router 2", "Red Hat", 25),
    ("Router 2", "Guaraní", 9),
    ("Router 2", "Router 3", 50),
    ("Router 3", "Switch 2", 61),
    ("Switch 2", "Manjaro", 40),
    ("Switch 2", "Parrot", 12),
    ("Switch 2", "MongoDB", 5),
    ("Switch 2", "Arch", 56),
    ("Switch 2", "Fedora", 3),
]


def cargar_red():
    g = Grafo(dirigido=False)  # h. grafo no dirigido
    for nombre, tipo in EQUIPOS.items():
        g.insertar_vertice(nombre, tipo=tipo)
    for u, v, p in ARISTAS:
        g.insertar_arista(u, v, p)
    return g


def titulo(texto):
    print(f"\n{'=' * 60}\n{texto}\n{'=' * 60}")


def punto_b(g):
    for nb in ("Red Hat", "Debian", "Arch"):
        print(f"\nDesde {nb} ({g.tipo(nb)}):")
        print("  Profundidad:", " -> ".join(g.barrido_profundidad(nb)))
        print("  Amplitud:   ", " -> ".join(g.barrido_amplitud(nb)))


def mejor_origen(g, origenes, destino):
    """Calcula el camino de cada origen al destino y devuelve el más corto."""
    mejor = None
    for o in origenes:
        camino, costo = g.camino_mas_corto(o, destino)
        print(f"  {o:8} -> {destino}: {costo:3}  ({' -> '.join(camino)})")
        if mejor is None or costo < mejor[1]:
            mejor = (o, costo, camino)
    return mejor


def main():
    g = cargar_red()

    titulo("a. Equipos y su tipo")
    for nombre, datos in g.vertices.items():
        print(f"  {nombre:10} {datos['tipo']}")

    titulo("b. Barridos en profundidad y amplitud")
    punto_b(g)

    titulo("c. Camino más corto hasta la impresora")
    for origen in ("Manjaro", "Red Hat", "Fedora"):
        camino, costo = g.camino_mas_corto(origen, "Impresora")
        print(f"  {origen:8}: {' -> '.join(camino)}  (costo {costo})")

    titulo("d. Árbol de expansión mínima (Kruskal)")
    arbol, total = g.kruskal()
    for u, v, p in arbol:
        print(f"  {u} - {v}: {p}")
    print(f"  Peso total: {total}")

    titulo("e. PC (no notebook) más cercana al servidor Guaraní")
    pcs = [v for v in g.vertices if g.tipo(v) == "pc"]
    o, costo, camino = mejor_origen(g, pcs, "Guaraní")
    print(f"  => La más cercana es {o} con costo {costo}")

    titulo("f. Computadora del Switch 1 más cercana a MongoDB")
    compus_sw1 = [v for v in g.vecinos("Switch 1")
                  if g.tipo(v) in ("pc", "notebook")]
    o, costo, camino = mejor_origen(g, compus_sw1, "MongoDB")
    print(f"  => La más cercana es {o} con costo {costo}")

    titulo("g. Impresora conectada al Router 2 y nuevo barrido (punto b)")
    peso = g.adyacentes["Switch 1"]["Impresora"]
    g.eliminar_arista("Switch 1", "Impresora")
    g.insertar_arista("Router 2", "Impresora", peso)
    print(f"  Impresora ahora conectada a Router 2 (peso {peso})")
    punto_b(g)


if __name__ == "__main__":
    main()
