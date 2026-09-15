import math
#ejercicio a
def vectorBase(n):
    v=[]
    for i in range(n):
        v.append(1/n) 
    return v

def vector_estacionario(matriz_transicion,n):
    antV= []
    V = vectorBase(n)
    while antV != V:
        antV = V.copy()
        for i in range(len(matriz_transicion)):
            suma=0
            for j in range(len(matriz_transicion)):
                suma+= antV[j]* matriz_transicion[i][j]
            V.append(suma)

    return V

#ejercicio b
def calcular_entropia(matriz_transicion,v):
    entropia=0
    for j in range(len(matriz_transicion)):
        suma=0
        for i in range(len(matriz_transicion)):
            suma += matriz_transicion[i][j] * (-1) * math.log2(matriz_transicion[i][j])
        entropia += suma * v[j]
    return entropia