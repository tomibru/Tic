from math import log2
# ---------------------------------------------------------------- Huffman
def huffman(probs):
    items = [[p, ""] for p in probs]          # [probabilidad, código]
    if len(items) == 1:
        return ["0"]

    # Cada nodo: [probabilidad acumulada, ítems (hojas) que contiene]
    nodos = [[item[0], [item]] for item in items]

    while len(nodos) > 1:
        nodos.sort(key=lambda n: n[0])        # ordenar de menor a mayor
        menor, siguiente = nodos.pop(0), nodos.pop(0)

        for item in menor[1]:                 # la menos probable recibe 0
            item[1] = "0" + item[1]
        for item in siguiente[1]:             # la otra recibe 1
            item[1] = "1" + item[1]

        # Se fusionan en un nuevo nodo y se vuelve a insertar
        nodos.append([menor[0] + siguiente[0], menor[1] + siguiente[1]])

    return [code for _, code in items]


# ----------------------------------------------------------- Shannon-Fano
def _codificar(items):
    """items: lista de [p, código] ordenada de mayor a menor probabilidad."""
    if len(items) <= 1:
        return

    total = sum(p for p, _ in items)

    # Buscar el corte que deja ambos grupos con probabilidades más parecidas
    acumulado, mejor_corte, mejor_dif = 0.0, 1, float("inf")
    for i in range(1, len(items)):
        acumulado += items[i - 1][0]
        dif = abs(acumulado - (total - acumulado))
        if dif < mejor_dif:
            mejor_dif, mejor_corte = dif, i

    for item in items[:mejor_corte]:          # grupo más probable -> 1
        item[1] += "1"
    for item in items[mejor_corte:]:          # grupo menos probable -> 0
        item[1] += "0"

    _codificar(items[:mejor_corte])
    _codificar(items[mejor_corte:])


def shannon_fano(probs):
    items = [[p, ""] for p in probs]
    if len(items) == 1:
        return ["0"]
    # sorted crea una lista nueva, pero con los mismos pares: se modifican in situ
    _codificar(sorted(items, key=lambda it: it[0], reverse=True))
    return [code for _, code in items]


# ------------------------------------------------------------- Utilidades
def metricas(probs, codigos):
    H = -sum(p * log2(p) for p in probs if p > 0)
    L = sum(p * len(c) for p, c in zip(probs, codigos))
    return H, L, H / L, 1 - H / L


def mostrar(probs, simbolos=None):
    """Muestra los códigos de Huffman y Shannon-Fano para cualquier fuente.

    probs:    lista de probabilidades.
    simbolos: nombres de los símbolos (opcional; por defecto S1, S2, ...).
    """
    if simbolos is None:
        simbolos = [f"S{i + 1}" for i in range(len(probs))]

    for nombre, f in (("Huffman", huffman), ("Shannon-Fano", shannon_fano)):
        codigos = f(probs)
        H, L, eta, R = metricas(probs, codigos)
        print(f"\n=== {nombre} ===")
        print(f"{'Símbolo':<10}{'P':<8}{'Código'}")
        for s, p, c in zip(simbolos, probs, codigos):
            print(f"{s:<10}{p:<8.2f}{c}")
        print(f"H(S) = {H:.4f} bits | L = {L:.4f} bits | "
              f"η = {eta:.4f} | R = {R:.4f}")

from extrearSyP import extraer_alfabeto_y_probabilidades

if __name__ == "__main__":
    probs = [ 0.385, 0.154, 0.128, 0.154, 0.179 ]
    mostrar(probs)

    mensaje = "58784784525368669895745123656253698989656452121702300223659"
    s ,p = extraer_alfabeto_y_probabilidades(mensaje)
    mostrar(p,s)