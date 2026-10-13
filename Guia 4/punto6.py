"""6. Realizar una función en Python que reciba como parámetros: dos listas paralelas con la 
distribución de probabilidades de una fuente y su codificación, y calcule el rendimiento y la 
redundancia del código."""
from math import log
def extraer_alfabeto_codigo(c):
    alfa = []
    for codigo in c:
        for simbolo in codigo:
            if simbolo not in alfa:
                alfa.append(simbolo)
    return sorted(alfa)

def rendimiento_y_redundancia(probs, x, cods):
    r = len(x)
    entropia = sum(-p * log(p,r) for p in probs)
    Lmedia = sum(p* len(c) for p,c in zip(probs, cods))

    return entropia/Lmedia, 1- entropia/Lmedia