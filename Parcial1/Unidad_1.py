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

import math
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

def vectorBase(n):
    v=[]
    for i in range(n):
        v.append(1/n) 
    return v

def vector_estacionario(matrizTransicion,n):
    antV= []
    V = vectorBase(n)
    while antV != V:
        antV = V.copy()
        V= []
        for i in range(len(matrizTransicion)):
            suma=0
            for j in range(len(matrizTransicion)):
                suma+= antV[j]* matrizTransicion[i][j]
            V.append(suma)

    return V


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

#.;.:.:.::;:,::.;:,::,;,:;.:.;.;;:,.::.:,.:.;:::::.
#")[))[([()))()[[]](([[)))])))][))(][)[[[)()]))[)[])"
mensaje = ";;,;,;:,,,.;,,.,,,::,;;;,:;.,,;:,,,:..;,;;.,;,,.:;"

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

vectorEstacionario = vector_estacionario(MatrizTransicion, len(alfabeto))

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

