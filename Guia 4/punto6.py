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

def rendimiento_y_redundancia(probs, cods):
    x = extraer_alfabeto_codigo(cods)
    r = len(x)
    entropia = sum(-p * log(p,r) for p in probs if p>0)
    Lmedia = sum(p* len(c) for p,c in zip(probs, cods))

    return entropia/Lmedia, 1- entropia/Lmedia
def extensioProbs(probs, n):
    pn = [1]
    for _ in range(n):
        nueva = []
        for e in pn:
            for p in probs:
                nueva.append(e * p)
        pn = nueva
    return pn


P1  = [0.5, 0.2, 0.3]
P2 = extensioProbs(P1, 2)
C1 = ["11", "010", "00"]
C2 = ["10", "001", "110", "010", "0000", "0001", "111", "0110", "0111"]

print(rendimiento_y_redundancia(P1, C1))
print(rendimiento_y_redundancia(P2, C2))
print("\n")
print("="*10 + "Punto 8" + "="*10)

P = [0.2, 0.15, 0.1, 0.3, 0.25]   # A, B, C, D, E

codigo1 = ["01", "111", "110", "101", "100"]
codigo2 = ["00", "01", "10", "110", "111"]
codigo3 = ["0110", "010", "0111", "1", "00"]
codigo4 = ["11", "001", "000", "10", "01"]

print(rendimiento_y_redundancia(P, codigo1))
print(rendimiento_y_redundancia(P, codigo2))
print(rendimiento_y_redundancia(P, codigo3))
print(rendimiento_y_redundancia(P, codigo4))