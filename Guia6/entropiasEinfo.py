import math


# ==================================================
# 1. PROBABILIDADES
# ==================================================

def probs_salida(priori, matriz):
    salida = []

    for j in range(len(matriz[0])):
        suma = 0
        for i in range(len(matriz)):
            suma += priori[i] * matriz[i][j]
        salida.append(suma)

    return salida


def probabilidadesPosteriori(priori, matriz):
    probabilidades_salida = probs_salida(priori, matriz)
    posteriori = []

    for i in range(len(matriz)):
        fila = []

        for j in range(len(matriz[0])):
            if probabilidades_salida[j] > 0:
                prob = (priori[i] * matriz[i][j]) / probabilidades_salida[j]
            else:
                prob = 0

            fila.append(prob)

        posteriori.append(fila)

    return posteriori


def probabilidadesSimultaneas(priori, matriz):
    simultaneas = []

    for i in range(len(matriz)):
        fila = []

        for j in range(len(matriz[0])):
            prob = priori[i] * matriz[i][j]
            fila.append(prob)

        simultaneas.append(fila)

    return simultaneas


# ==================================================
# 2. ENTROPIAS
# ==================================================

# --------------------------------------------------
# 2.1 ENTROPIA A PRIORI: H(A)
# --------------------------------------------------

def entropiaApriori(priori):
    suma = 0

    for p in priori:
        if p > 0:
            suma += p * math.log2(1 / p)

    return suma


# --------------------------------------------------
# 2.2 ENTROPIA DE SALIDA: H(B)
# --------------------------------------------------

def entropiaSalida(priori, matriz):
    salida = probs_salida(priori, matriz)
    suma = 0

    for p in salida:
        if p > 0:
            suma += p * math.log2(1 / p)

    return suma


# --------------------------------------------------
# 2.3 ENTROPIA A POSTERIORI PUNTUAL: H(A/bj)
# --------------------------------------------------

def entropiaPosterioriPuntual(priori, matriz, j):
    posteriori = probabilidadesPosteriori(priori, matriz)
    suma = 0

    for i in range(len(matriz)):
        prob = posteriori[i][j]

        if prob > 0:
            suma += prob * math.log2(1 / prob)

    return suma


# --------------------------------------------------
# 2.4 ENTROPIAS A POSTERIORI: H(A/bj)
# --------------------------------------------------

def entropiasPosteriori(priori, matriz):
    entropias = []

    for j in range(len(matriz[0])):
        entropia = entropiaPosterioriPuntual(priori, matriz, j)
        entropias.append(entropia)

    return entropias


# --------------------------------------------------
# 2.5 EQUIVOCACION: H(A/B)
# --------------------------------------------------

def equivocacion(priori, matriz):
    salida = probs_salida(priori, matriz)
    entropias = entropiasPosteriori(priori, matriz)
    suma = 0

    for j in range(len(matriz[0])):
        suma += salida[j] * entropias[j]

    return suma


# --------------------------------------------------
# 2.6 PERDIDA O RUIDO DIRECTO: H(B/A)
# --------------------------------------------------

def perdida(priori, matriz):
    suma = 0

    for i in range(len(matriz)):
        entropia = 0

        for j in range(len(matriz[0])):
            prob = matriz[i][j]

            if prob > 0:
                entropia += prob * math.log2(1 / prob)

        suma += priori[i] * entropia

    return suma


# --------------------------------------------------
# 2.7 ENTROPIA AFIN O CONJUNTA: H(A,B)
# --------------------------------------------------

def entropiaAfin(priori, matriz):
    simultaneas = probabilidadesSimultaneas(priori, matriz)
    suma = 0

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            prob = simultaneas[i][j]

            if prob > 0:
                suma += prob * math.log2(1 / prob)

    return suma


# --------------------------------------------------
# 2.8 INFORMACION MUTUA: I(A,B)
# --------------------------------------------------

def informacionMutua(priori, matriz):
    simultaneas = probabilidadesSimultaneas(priori, matriz)
    salida = probs_salida(priori, matriz)

    suma = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            conjunta = simultaneas[i][j]

            if conjunta > 0:
                suma += conjunta * math.log2(
                    conjunta / (priori[i] * salida[j])
                )

    return suma


# ==================================================
# 3. PRUEBAS
# ==================================================

priori = [ 0.25, 0.50, 0.25]

matriz = [
    [ 1.0, 0.0, 0.0, 0.0 ],
    [ 0.0, 0.5 ,0.5 ,0.0 ],
    [ 0.0, 0.0, 0.0, 1.0 ]
]


# --------------------------------------------------
# 3.1 PROBABILIDADES
# --------------------------------------------------

print("\n========== PROBABILIDADES ==========")

print("Probabilidades a priori:")
print(priori)

print("\nProbabilidades de salida:")
print(probs_salida(priori, matriz))

print("\nProbabilidades a posteriori:")
matriz_post = probabilidadesPosteriori(priori, matriz)

for fila in matriz_post:
    print(fila)

print("\nProbabilidades simultaneas:")
print(probabilidadesSimultaneas(priori, matriz))


# --------------------------------------------------
# 3.2 ENTROPIAS
# --------------------------------------------------

print("\n========== ENTROPIAS ==========")

print("Entropia a priori H(A):")
print(entropiaApriori(priori))

print("\nEntropia de salida H(B):")
print(entropiaSalida(priori, matriz))

print("\nEntropias a posteriori puntuales:")

for j in range(len(matriz[0])):
    print("H(A/b" + str(j + 1) + "):",
          entropiaPosterioriPuntual(priori, matriz, j))

print("\nLista de entropias a posteriori:")
print(entropiasPosteriori(priori, matriz))

print("\nEquivocacion H(A/B):")
print(equivocacion(priori, matriz))

print("\nPerdida H(B/A):")
print(perdida(priori, matriz))

print("\nEntropia afin H(A,B):")
print(entropiaAfin(priori, matriz))

print("\nInformacion mutua I(A,B):")
print(informacionMutua(priori, matriz))


# --------------------------------------------------
# 3.3 VERIFICACION DE RELACIONES
# --------------------------------------------------

print("\n========== VERIFICACION ==========")

print("H(A) = H(A/B) + I(A,B):")
print(entropiaApriori(priori),
      "=",
      equivocacion(priori, matriz) + informacionMutua(priori, matriz))

print("\nH(B) = H(B/A) + I(A,B):")
print(entropiaSalida(priori, matriz),
      "=",
      perdida(priori, matriz) + informacionMutua(priori, matriz))

print("\nH(A,B) = H(A) + H(B/A):")
print(entropiaAfin(priori, matriz),
      "=",
      entropiaApriori(priori) + perdida(priori, matriz))

print("\nH(A,B) = H(B) + H(A/B):")
print(entropiaAfin(priori, matriz),
      "=",
      entropiaSalida(priori, matriz) + equivocacion(priori, matriz))