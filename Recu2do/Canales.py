import math
Matriz_canal = [[0.0, 0.0, 1.0], [0.4, 0.4, 0.2]]

def generarDistribuciones(cantidad, unidades):
    if cantidad == 1:
        return [[unidades]]

    distribuciones = []

    for i in range(unidades + 1):
        restantes = generarDistribuciones(
            cantidad - 1, unidades - i
        )

        for distribucion in restantes:
            nueva = [i]

            for p in distribucion:
                nueva.append(p)

            distribuciones.append(nueva)

    return [
        [p / unidades for p in distribucion]
        for distribucion in distribuciones
    ]

def probabilidadesSimultaneas(priori, matriz):
    simultaneas = []

    for i in range(len(matriz)):
        fila = []

        for j in range(len(matriz[0])):
            prob = priori[i] * matriz[i][j]
            fila.append(prob)

        simultaneas.append(fila)

    return simultaneas


def probs_salida(priori, matriz):
    salida = []

    for j in range(len(matriz[0])):
        suma = 0
        for i in range(len(matriz)):
            suma += priori[i] * matriz[i][j]
        salida.append(suma)

    return salida

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

def capacidadEstimada(matriz, paso):
    if paso <= 0 or paso > 1:
        raise ValueError("El paso debe estar entre 0 y 1.")

    cantidad_entradas = len(matriz)

    unidades = math.ceil(1 / paso)

    distribuciones = generarDistribuciones(
        cantidad_entradas, unidades
    )

    capacidad = -1
    mejorProbabilidad = []

    for priori in distribuciones:
        info = informacionMutua(priori, matriz)

        if info > capacidad:
            capacidad = info
            mejorProbabilidad = priori

    return capacidad, mejorProbabilidad

paso = 0.001

print("\nCapacidad estimada del canal:")
capacidad, mejorProbabilidad = capacidadEstimada(Matriz_canal, paso)
print(f"Capacidad: {capacidad:.4f}")
print(f"Mejor distribución a priori: {mejorProbabilidad}")

# ==================================================
# 2. PROBABILIDADES DE SALIDA, POSTERIORES Y CONJUNTAS
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
                prob = (
                    priori[i] * matriz[i][j]
                    / probabilidades_salida[j]
                )
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
# 3. ENTROPIAS E INFORMACION MUTUA
# ==================================================

def entropiaApriori(priori):
    suma = 0

    for p in priori:
        if p > 0:
            suma += p * math.log2(1 / p)

    return suma


def entropiaSalida(priori, matriz):
    salida = probs_salida(priori, matriz)
    return entropiaApriori(salida)


def entropiaPosterioriPuntual(priori, matriz, j):
    posteriori = probabilidadesPosteriori(priori, matriz)

    suma = 0

    for i in range(len(matriz)):
        prob = posteriori[i][j]

        if prob > 0:
            suma += prob * math.log2(1 / prob)

    return suma


def entropiasPosteriori(priori, matriz):
    entropias = []

    for j in range(len(matriz[0])):
        entropia = entropiaPosterioriPuntual(
            priori, matriz, j
        )

        entropias.append(entropia)

    return entropias


# Equivocacion: H(A|B)
def equivocacion(priori, matriz):
    salida = probs_salida(priori, matriz)
    entropias = entropiasPosteriori(priori, matriz)

    suma = 0

    for j in range(len(matriz[0])):
        suma += salida[j] * entropias[j]

    return suma


# Perdida: H(B|A)
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

print("\n")
print("=" * 55)
print("       C) METRICAS DEL CANAL")
print("=" * 55)

H_A = entropiaApriori(mejorProbabilidad)
H_B = entropiaSalida(mejorProbabilidad, Matriz_canal)
H_A_B = equivocacion(mejorProbabilidad, Matriz_canal)
H_B_A = perdida(mejorProbabilidad, Matriz_canal)
I_AB = informacionMutua(mejorProbabilidad, Matriz_canal)

print(f"\nEntropia de entrada H(A):       {H_A:.4f} bits")
print(f"Entropia de salida H(B):        {H_B:.4f} bits")
print(f"Equivocacion H(A|B):            {H_A_B:.4f} bits")
print(f"Perdida H(B|A):                 {H_B_A:.4f} bits")
print(f"Informacion mutua I(A;B):       {I_AB:.4f} bits")

