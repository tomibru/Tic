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

def entropiaApriori(priori):
    return sum(-p* math.log2(p) for p in priori)


def entropiasPosteriori(priori, matriz):
    posteriori = probabilidadesPosteriori(priori, matriz)
    entropias = []

    for j in range(len(matriz[0])):
        suma = 0

        for i in range(len(matriz)):
            prob = posteriori[i][j]

            if prob > 0:
                suma += prob * math.log2(prob)

        entropias.append(-suma)

    return entropias


def equivocacion(priori, matriz):
    posteriori = probabilidadesPosteriori(priori, matriz)
    simultaneas = probabilidadesSimultaneas(priori, matriz)
    suma = 0

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if simultaneas[i][j] > 0:
                suma += simultaneas[i][j] * math.log2(1 / posteriori[i][j])

    return suma


def perdida(priori, matriz):
    simultaneas = probabilidadesSimultaneas(priori, matriz)
    suma = 0

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if simultaneas[i][j] > 0:
                suma += simultaneas[i][j] * math.log2(1 / matriz[i][j])

    return suma


def entropiaAfin(priori, matriz):
    simultaneas = probabilidadesSimultaneas(priori, matriz)
    suma = 0

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if simultaneas[i][j] > 0:
                suma += simultaneas[i][j] * math.log2(1 / simultaneas[i][j])

    return suma


def informacionMutua(priori, matriz):
    salida = probs_salida(priori, matriz)
    simultaneas = probabilidadesSimultaneas(priori, matriz)
    suma = 0

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            if simultaneas[i][j] > 0:
                prob = simultaneas[i][j] / (priori[i] * salida[j])
                suma += simultaneas[i][j] * math.log2(prob)

    return suma


# ==================================================
# 3. CLASIFICACIÓN DE CANALES
# ==================================================

def esSinRuido(matriz):
    for j in range(len(matriz[0])):
        cont = 0

        for i in range(len(matriz)):
            if matriz[i][j] != 0:
                cont += 1

        if cont != 1:
            return False

    return True


def esDeterminante(matriz):
    for i in range(len(matriz)):
        cont = 0

        for j in range(len(matriz[0])):
            if matriz[i][j] != 0:
                cont += 1

        if cont != 1:
            return False

    return True


# ==================================================
# 4. COMPOSICIÓN Y REDUCCIÓN DE CANALES
# ==================================================

def canalCompuesto(M1, M2):
    compuesto = []

    for i in range(len(M1)):
        fila = []

        for j in range(len(M2[0])):
            suma = 0

            for k in range(len(M2)):
                suma += M1[i][k] * M2[k][j]

            fila.append(suma)

        compuesto.append(fila)

    return compuesto


def sePuedenCombinar(matriz, col1, col2):
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            if abs(matriz[i][col1] * matriz[j][col2] -
                   matriz[j][col1] * matriz[i][col2]) > 1e-9:
                return False

    return True


def canalDeterminante(matriz, col1, col2):
    determinante = []

    for i in range(len(matriz[0])):
        fila = []

        if i == col1 or i == col2:
            fila.append(1)
        else:
            fila.append(0)

        for j in range(len(matriz[0])):
            if j != col1 and j != col2:
                if i == j:
                    fila.append(1)
                else:
                    fila.append(0)

        determinante.append(fila)

    return determinante


def reducirCanal(matriz):
    reducida = matriz
    seguir = True

    while seguir:
        seguir = False

        for i in range(len(reducida[0])):
            for j in range(i + 1, len(reducida[0])):
                if sePuedenCombinar(reducida, i, j):
                    determinante = canalDeterminante(reducida, i, j)
                    reducida = canalCompuesto(reducida, determinante)
                    seguir = True
                    break

            if seguir:
                break

    return reducida


# ==================================================
# 5. CANALES UNIFORMES
# ==================================================

def esUniforme(matriz):
    sumaAnterior = 0

    for i in range(len(matriz)):
        sumaAnterior += matriz[i][0]

    for j in range(1, len(matriz[0])):
        suma = 0

        for i in range(len(matriz)):
            suma += matriz[i][j]

        if abs(suma - sumaAnterior) > 1e-9:
            return False

    return True


# ==================================================
# 6. CAPACIDAD DE CANALES
# ==================================================

def capacidadDeterminante(matriz):
    return math.log2(len(matriz[0]))


def capacidadSinRuido(matriz):
    return math.log2(len(matriz))


def capacidadUniforme(priori, matriz):
    return math.log2(len(matriz[0])) - perdida(priori, matriz)


def capacidadEstimada(matriz, paso):
    if paso <= 0 or paso > 1:
        raise ValueError("El paso debe ser mayor que 0 y menor o igual que 1")

    capacidad = -1
    mejorProbabilidad = []
    i = 0

    while i * paso <= 1:
        p = i * paso
        priori = [p, 1 - p]

        info = informacionMutua(priori, matriz)

        if info > capacidad:
            capacidad = info
            mejorProbabilidad = priori

        i += 1

    return capacidad, mejorProbabilidad


# ==================================================
# 7. PROBABILIDAD DE ERROR
# ==================================================

def probabilidadError(priori, matriz):
    posteriori = probabilidadesPosteriori(priori, matriz)
    salida = probs_salida(priori, matriz)
    error = 0

    for j in range(len(matriz[0])):
        mayor = 0

        for i in range(len(matriz)):
            if posteriori[i][j] > mayor:
                mayor = posteriori[i][j]

        error += salida[j] * (1 - mayor)

    return error


# ==================================================
# 8. PRUEBAS
# ==================================================

# --------------------------------------------------
# 8.1 PROBABILIDADES
# --------------------------------------------------

print("\n========== 1. PROBABILIDADES ==========")
#from MatrizTransicionCanal import matrizCanal, extraer_priori, extraer_alfabeto

#entrada = "abcacaabbcacaabcacaaabcaca"
#salida = "01010110011001000100010011"
#priori = extraer_priori(entrada)
#matriz = matrizCanal(entrada , salida)

priori =  [0.5, 0.5]
matriz = [
    [0.3,0.3,0.4], 
    [0.3,0.3,0.4]
]

print("Probabilidades de salida:")
print(probs_salida(priori, matriz))

print("\nProbabilidades a posteriori:")
matriz_post = probabilidadesPosteriori(priori, matriz)
for i in range(len(matriz_post)):
    print(matriz_post[i],"\n")

print("\nProbabilidades simultáneas:")
print(probabilidadesSimultaneas(priori, matriz))


# --------------------------------------------------
# 8.2 ENTROPIAS
# --------------------------------------------------

print("\n========== 2. ENTROPIAS ==========")

print("Entropías a priori:")
print(entropiaApriori(priori))

print("Entropías a posteriori:")
print(entropiasPosteriori(priori, matriz))

print("\nEquivocación o ruido:")
print(equivocacion(priori, matriz))

print("\nPérdida:")
print(perdida(priori, matriz))

print("\nEntropía afín:")
print(entropiaAfin(priori, matriz))

print("\nInformación mutua:")
print(informacionMutua(priori, matriz))


# --------------------------------------------------
# 8.3 CLASIFICACIÓN DE CANALES
# --------------------------------------------------

print("\n========== 3. CLASIFICACIÓN DE CANALES ==========")

canal = [
    [1, 0, 0],
    [0, 0.5, 0.5],
    [0, 0, 1]
]

print("Canal de prueba:")
print(canal)

print("\n¿Es un canal sin ruido?")
print(esSinRuido(canal))

print("\n¿Es un canal determinante?")
print(esDeterminante(canal))


# --------------------------------------------------
# 8.4 COMPOSICIÓN Y REDUCCIÓN
# --------------------------------------------------

print("\n========== 4. COMPOSICIÓN Y REDUCCIÓN ==========")

M1 = [
    [0.2, 0.1, 0.7],
    [0.4, 0.2, 0.4],
    [0.6, 0.3, 0.1]
]

M2 = canalDeterminante(M1, 0, 1)

print("Matriz original:")
print(M1)

print("\n¿Se pueden combinar las columnas 0 y 1?")
print(sePuedenCombinar(M1, 0, 1))

print("\nCanal determinante para combinar:")
print(M2)

print("\nCanal compuesto:")
print(canalCompuesto(M1, M2))

print("\nCanal reducido:")
print(reducirCanal(M1))


# --------------------------------------------------
# 8.5 CANALES UNIFORMES
# --------------------------------------------------

print("\n========== 5. CANALES UNIFORMES ==========")

uniforme = [
    [0.9, 0.1],
    [0.1, 0.9]
]

print("Matriz del canal:")
print(uniforme)

print("\n¿Es un canal uniforme?")
print(esUniforme(uniforme))


# --------------------------------------------------
# 8.6 CAPACIDAD DE CANALES
# --------------------------------------------------

print("\n========== 6. CAPACIDAD DE CANALES ==========")

determinante = [
    [1, 0],
    [0, 1]
]

sinRuido = [
    [1, 0],
    [0, 1]
]

print("Capacidad del canal determinante:")
print(capacidadDeterminante(determinante))

print("\nCapacidad del canal sin ruido:")
print(capacidadSinRuido(sinRuido))

prioriUniforme = [0.5, 0.5]

print("\nCapacidad del canal uniforme:")
print(capacidadUniforme(prioriUniforme, uniforme))

print("\nCapacidad estimada del canal binario:")
print(capacidadEstimada(uniforme, 0.1))


# --------------------------------------------------
# 8.7 PROBABILIDAD DE ERROR
# --------------------------------------------------

print("\n========== 7. PROBABILIDAD DE ERROR ==========")

print("Probabilidad de error:")
print(probabilidadError(priori, matriz))