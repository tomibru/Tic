import math
print("\n")
print("-"*20 + "UNIDAD  2" + "-"*20)
"""  
ALFABETO Y PROBABILIDADES:
    - Se identificaron los símbolos únicos del mensaje S = {S1, ..., Sn}.
    - P(Si) = n_i / N, donde n_i es la frecuencia del símbolo Si y N la longitud
      total de la cadena de entrada.
"""

def extraer_alfabeto_y_probabilidades(mensaje):
    alfabeto = []
    probabilidades = []
    frecuencias = {}
    totalChar = len(mensaje)
    if totalChar == 0:
        return [],[];
    else:
        for simbolo in mensaje:
            if simbolo in frecuencias:
                frecuencias[simbolo] = frecuencias[simbolo] +1
            else:
                frecuencias[simbolo] = 1

        for simbolo in sorted(frecuencias.keys()):
            alfabeto.append(simbolo)
            probabilidades.append(frecuencias[simbolo] / totalChar)
        return alfabeto, probabilidades

def inicializarMatriz(n):
    matriz = []
    for i in range(n):
        fila =[]
        for j in range(n):
            fila.append(0)
        matriz.append(fila)
    return matriz

"""
MATRIZ TRANSICION:

Para construir la matriz de transición condicional P(S_i | S_j) ,
se contabilizó la frecuencia absoluta de transiciones N(S_j --> S_i). 
Posicionamiento: S_j (estado previo) representa la columna y S_i (estado posterior) representa 
a fila.
Cálculo: La probabilidad condicional se obtiene dividiendo el número de pares (S_j, S_i) por 
la cantidad total de veces que se emitió el símbolo inicial S_j

Entonces P(S_i | S_j) = N(S_j --> S_i)/N(S_j)
"""
def Matriz_Transicion(cadena, alfabeto):
  transiciones = {}
  salidas = {}

  for i in range(len(cadena) - 1):
    actual = cadena[i]
    siguiente = cadena[i + 1]

    if actual in salidas:
      salidas[actual] += 1
    else:
      salidas[actual] = 1

    if (actual, siguiente) in transiciones:
      transiciones[(actual, siguiente)] += 1
    else:
      transiciones[(actual, siguiente)] = 1

  M = inicializarMatriz(len(alfabeto))

  for transicion in transiciones:
    actual = transicion[0]
    siguiente = transicion[1]

    fila = alfabeto.index(siguiente)
    columna = alfabeto.index(actual)

    M[fila][columna] = transiciones[transicion] / salidas[actual]

  return M

"""
Estimacion de memoria:

Para determinar si la fuente es de memoria nula o no se comparo cada columna de la 
matriz de transicion con las probabilidades de cada simbolo con una tolerancia 
preestablecida en este caso de 0.02. Si para todo elemento de la matriz se cumple que
| M[i,j] - Probs[i] | <= 0.02 entonces podemos considerar a la fuente de memoria nula, 
en caso contrario sera fuente con memoria.
"""

def es_fuente_memoria_nula(matriz, probabilidades, tolerancia):
  n = len(probabilidades)

  for j in range(n):
    # Extraemos la columna j (transiciones desde el símbolo j)
    columna_j = [matriz[i][j] for i in range(n)]

    # Verificamos si la columna j es igual a la lista de probabilidades
    for i in range(n):
      if abs(columna_j[i] - probabilidades[i]) > tolerancia:
        return False

  return True


"""
Entropia:

Dependiendo del tipo de fuente se aplican sus respectivas formulas 
    Memoria nula:
        H(S) = sum(P(S_i) * -log_2(P(S_i)))
    Con memoria:
        H(S) = sum( P_i * H(S|Si) )
        donde H(S|Si) = - sum( P(Sj|Si) * log2(P(Sj|Si)) ) y P_i son las
        componentes del vector estacionario.
"""

def entropia(probs, M, V):
    r=2
    if es_fuente_memoria_nula(M, probs, 0.02):
        suma=0
        for p in probs:
            suma += p * -math.log(p,r)
        return suma
    else:
        h1 =0
        for i in range(len(V)):
            suma_condicional=0
            p_i_estacionaria = V[i]
            for j in range(len(V)):
                p_j_dado_i = M[j][i]
                if p_j_dado_i > 0:
                    suma_condicional +=  p_j_dado_i * -math.log(p_j_dado_i, r) 
            h1 += suma_condicional * p_i_estacionaria
        return h1    

"""
Vector estacionario:

La distribución de probabilidades en cada t (vectores de estado) va variando con la 
evolución del proceso de emisión de símbolos, hasta estabilizarse en el estado estacionario. 


Se inicializa un vector base, cada elemento en 1/n, 
se multiplica con la matriz de forma consecutiva hasta que la diferencia entre su version 
anterior y la nueva difieran como maximo en una tolerancia de 1x10^-9 y realizando maximo de 
iteraciones de 2000.
"""
  

def vectorBase(n):
    v=[]
    for i in range(n):
        v.append(1/n) 
    return v

def vector_estacionario(matrizTransicion,n, tolerancia):
    antV= []
    V = vectorBase(n)
    distintos = True
    iteraciones =0
    while distintos or iteraciones < 2000:
        iteraciones += 1
        antV = V.copy()
        V= []
        for i in range(len(matrizTransicion)):
            suma=0
            for j in range(len(matrizTransicion)):
                suma+= antV[j]* matrizTransicion[i][j]
            V.append(suma)
        elementos = 0
        while elementos < len(V) and abs(antV[elementos] - V[elementos]) < tolerancia:
            elementos += 1
        if elementos == len(V):
            distintos = False

    return V

"""
Extensión de Orden N (Si es Memoria Nula):
Se generaron todas las combinaciones posibles de pares de símbolos S^N 
Al ser memoria nula, la probabilidad de cada par es el producto de sus probabilidades marginales
La entropía de la extensión cumple H(S^N) = N * H(S).   
"""

def generar_combinaciones(alfabeto, n):
    combinaciones = [""]  # arranca con el bloque vacío

    for _ in range(n):
        nuevas_combinaciones = []
        for bloque in combinaciones:
            for letra in alfabeto:
                nuevas_combinaciones.append(bloque + letra)
        combinaciones = nuevas_combinaciones

    return combinaciones


def extensionN(alfabeto, probabilidades, n):
    probs_originales = {}
    for i in range(len(alfabeto)):
        letra = alfabeto[i]
        probs_originales[letra] = probabilidades[i]

    combinaciones = generar_combinaciones(alfabeto, n)
    alfaExt = []
    probExt = []

    for bloque in combinaciones:
        alfaExt.append(bloque)
        probAcumulada = 1.0
        for letra in bloque:
            probAcumulada = probAcumulada * probs_originales[letra]
        probExt.append(probAcumulada)

    return alfaExt, probExt

def es_fuente_ergodica(matriz, tolerancia):

    n = len(matriz)

    # Primero verificamos que sea irreducible
    for inicio in range(n):

        visitados = []
        por_visitar = [inicio]

        while len(por_visitar) > 0:

            actual = por_visitar.pop()

            if actual not in visitados:
                visitados.append(actual)

                # La columna actual representa desde donde salimos
                for siguiente in range(n):
                    if matriz[siguiente][actual] > tolerancia:
                        if siguiente not in visitados:
                            por_visitar.append(siguiente)

        # Si no pudimos llegar a todos los estados,
        # la fuente no es irreducible
        if len(visitados) != n:
            return False

    # Si es irreducible, verificamos que sea aperiódica
    for i in range(n):
        if matriz[i][i] > tolerancia:
            return True

    return False

#---------------MAIN----------------------------------------------------------------------

#.;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::.
#")[))[([()))()[[]](([[)))])))][))(][)[[[)()]))[)[])"
mensaje = ".;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::."

alfabeto, probabilidades = extraer_alfabeto_y_probabilidades(mensaje)
for a,p in zip(alfabeto,probabilidades):
    print("P( " + a + " ): " + str(p))
print("\n")

MatrizTransicion = Matriz_Transicion(mensaje, alfabeto)
print("Matriz de transición:")
print("      " + "  ".join(f"{s:>6}" for s in alfabeto))
for simbolo_fila, fila in zip(alfabeto, MatrizTransicion):
    print(f"{simbolo_fila:>3} " + "  ".join(f"{valor:.4f}" for valor in fila))
print("\n")

if es_fuente_memoria_nula(MatrizTransicion, probabilidades, 0.02):
   print("Fuente de memoria nula")
else:
   print("Fuente con memoria")
print("\n")

vectorEstacionario = vector_estacionario(MatrizTransicion, len(alfabeto), 1e-9)

print("Vector estacionario")
for n in vectorEstacionario:
    print(n)
print("\n")

print("Entropia :" , entropia(probabilidades, MatrizTransicion , vectorEstacionario))
print("\n")

#Extension orden n
n = 2
alfaExt, probExt = extensionN(alfabeto, probabilidades, n)

# Mostrar cada extensión junto a su probabilidad usando zip
print("Entropia extension: ", entropia(probabilidades, MatrizTransicion, vectorEstacionario) * n)
print(f"{'Extensión':<15} | {'Probabilidad':<12}")
print("-" * 30)

for simbolo, prob in zip(alfaExt, probExt):
    print(f"{simbolo:<15} | {prob:.4f}")
print("\n   ")

if es_fuente_ergodica(MatrizTransicion, 0.02):
    print("Fuente ergódica")
else:
    print("Fuente no ergódica")
