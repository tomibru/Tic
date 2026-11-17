
import math
# ==================================================
# 1. ALFABETOS, PROBABILIDADES Y MATRIZ DEL CANAL
# ==================================================

def extraer_alfabeto(c):
    return sorted(set(c))


def extraer_priori(entrada):
    if len(entrada) == 0:
        raise ValueError("La entrada no puede estar vacia.")

    alfa_entrada = extraer_alfabeto(entrada)
    probabilidades = []

    for simbolo in alfa_entrada:
        frecuencia = entrada.count(simbolo)
        probabilidades.append(frecuencia / len(entrada))

    return probabilidades


def matrizCanal(entrada, salida):
    alfa_entrada = extraer_alfabeto(entrada)
    alfa_salida = extraer_alfabeto(salida)

    matriz = []

    for i in range(len(alfa_entrada)):
        fila = []

        for j in range(len(alfa_salida)):
            fila.append(0)

        matriz.append(fila)

    # Contar las apariciones de cada par entrada/salida.
    for i in range(len(entrada)):
        simboloE = entrada[i]
        simboloS = salida[i]

        fila = alfa_entrada.index(simboloE)
        columna = alfa_salida.index(simboloS)

        matriz[fila][columna] += 1

    # Convertir las frecuencias en probabilidades condicionales.
    for i in range(len(alfa_entrada)):
        cantidad_entrada = entrada.count(alfa_entrada[i])

        for j in range(len(alfa_salida)):
            matriz[i][j] /= cantidad_entrada

    return matriz


def validarMatriz(matriz):
    if len(matriz) == 0 or len(matriz[0]) == 0:
        raise ValueError("La matriz no puede estar vacia.")

    cantidad_columnas = len(matriz[0])

    for fila in matriz:
        if len(fila) != cantidad_columnas:
            raise ValueError("Todas las filas deben tener igual longitud.")

        for probabilidad in fila:
            if probabilidad < 0:
                raise ValueError("No puede haber probabilidades negativas.")

        if abs(sum(fila) - 1) > 1e-9:
            raise ValueError("Cada fila de la matriz debe sumar 1.")


def imprimirMatriz(matriz, alfa_filas, alfa_columnas, titulo,
                   nombre_filas, nombre_columnas):

    print("\n" + titulo)
    print(f"Filas: {nombre_filas}")
    print(f"Columnas: {nombre_columnas}\n")

    encabezado = f"{nombre_filas} / {nombre_columnas}"
    print(f"{encabezado:<22}", end="")

    for simbolo in alfa_columnas:
        print(f"{simbolo:>10}", end="")

    print()

    for i in range(len(alfa_filas)):
        print(f"{alfa_filas[i]:<22}", end="")

        for j in range(len(alfa_columnas)):
            print(f"{matriz[i][j]:>10.4f}", end="")

        print()


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


# Entropia conjunta: H(A,B)
def entropiaAfin(priori, matriz):
    simultaneas = probabilidadesSimultaneas(priori, matriz)

    suma = 0

    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            prob = simultaneas[i][j]

            if prob > 0:
                suma += prob * math.log2(1 / prob)

    return suma


# Informacion mutua: I(A;B)
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
# 4. CLASIFICACION DE CANALES
# ==================================================

# Canal sin ruido:
# Cada salida posible puede provenir de una sola entrada.
def esSinRuido(matriz):
    for j in range(len(matriz[0])):
        cont = 0

        for i in range(len(matriz)):
            if matriz[i][j] > 0:
                cont += 1

        if cont > 1:
            return False

    return True


# Canal determinante:
# Cada entrada produce una unica salida con probabilidad 1.
def esDeterminante(matriz):
    for i in range(len(matriz)):
        cont = 0

        for j in range(len(matriz[0])):
            if matriz[i][j] > 0:
                cont += 1

        if cont != 1:
            return False

    return True


# ==================================================
# 5. COMPOSICION Y REDUCCION DE CANALES
# ==================================================

def canalCompuesto(M1, M2):
    if len(M1[0]) != len(M2):
        raise ValueError("Las dimensiones de las matrices no coinciden.")

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


# Comprueba si dos columnas son proporcionales.
def sePuedenCombinar(matriz, col1, col2):
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            determinante = (
                matriz[i][col1] * matriz[j][col2]
                - matriz[j][col1] * matriz[i][col2]
            )

            if abs(determinante) > 1e-9:
                return False

    return True


# Construye una matriz que agrupa dos columnas.
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
    reducida = [fila[:] for fila in matriz]

    seguir = True

    while seguir:
        seguir = False

        for i in range(len(reducida[0])):
            for j in range(i + 1, len(reducida[0])):

                if sePuedenCombinar(reducida, i, j):
                    determinante = canalDeterminante(
                        reducida, i, j
                    )

                    reducida = canalCompuesto(
                        reducida, determinante
                    )

                    seguir = True
                    break

            if seguir:
                break

    # Control: las filas de la matriz reducida deben sumar 1.
    validarMatriz(reducida)

    return reducida


# ==================================================
# 6. CAPACIDAD DEL CANAL
# ==================================================

# Genera distribuciones a priori posibles.
# Permite trabajar con cualquier cantidad de entradas.
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


# ==================================================
# 7. PROBABILIDAD DE ERROR
# ==================================================

# Error minimo utilizando la regla MAP.
# Se debe usar la distribucion a priori indicada en el ejercicio.
def probabilidadError(priori, matriz):
    simultaneas = probabilidadesSimultaneas(
        priori, matriz
    )

    suma_maximos = 0

    for j in range(len(matriz[0])):
        mayor = 0

        for i in range(len(matriz)):
            if simultaneas[i][j] > mayor:
                mayor = simultaneas[i][j]

        suma_maximos += mayor

    return 1 - suma_maximos


# ==================================================
# 9. DATOS DEL EJERCICIO
# ==================================================

entrada = "10100000101011101001111110011001"
salida = "QQPQQPPQQQPQRRRQSPQSQRQSQQPSQQPP"

if len(entrada) == 0 or len(salida) == 0:
    raise ValueError("Las secuencias no pueden estar vacias.")

if len(entrada) != len(salida):
    raise ValueError("Entrada y salida deben tener igual longitud.")


# Obtener alfabetos, probabilidades y matriz.
alfa_entrada = extraer_alfabeto(entrada)
alfa_salida = extraer_alfabeto(salida)

priori_probs = extraer_priori(entrada)
matriz_canal = matrizCanal(entrada, salida)



# ==================================================
# 10. PROBABILIDADES Y MATRICES
# ==================================================

print("\n")
print("=" * 55)
print("       A) PROBABILIDADES Y MATRICES")
print("=" * 55)

print("\nAlfabeto de entrada:", alfa_entrada)
print("Alfabeto de salida:", alfa_salida)

print("\nPROBABILIDADES A PRIORI")

for i in range(len(alfa_entrada)):
    print(f"P({alfa_entrada[i]}) = {priori_probs[i]:.4f}")


imprimirMatriz(
    matriz_canal,
    alfa_entrada,
    alfa_salida,
    "MATRIZ DEL CANAL P(B|A)",
    "Simbolos de entrada",
    "Simbolos de salida"
)


# Mostrar las probabilidades a posteriori como matriz.
posteriori = probabilidadesPosteriori(
    priori_probs, matriz_canal
)

imprimirMatriz(
    posteriori,
    alfa_entrada,
    alfa_salida,
    "MATRIZ DE PROBABILIDADES A POSTERIORI P(A|B)",
    "Simbolos de entrada",
    "Simbolos de salida"
)


# Mostrar probabilidades conjuntas.
conjuntas = probabilidadesSimultaneas(
    priori_probs, matriz_canal
)

imprimirMatriz(
    conjuntas,
    alfa_entrada,
    alfa_salida,
    "MATRIZ DE PROBABILIDADES CONJUNTAS P(A,B)",
    "Simbolos de entrada",
    "Simbolos de salida"
)


# Mostrar probabilidades de salida.
probabilidades_salida = probs_salida(
    priori_probs, matriz_canal
)

print("\nPROBABILIDADES DE SALIDA")

for j in range(len(alfa_salida)):
    print(
        f"P({alfa_salida[j]}) = "
        f"{probabilidades_salida[j]:.4f}"
    )


# ==================================================
# 11. CLASIFICACION DEL CANAL
# ==================================================

print("\n")
print("=" * 55)
print("       B) CLASIFICACION DEL CANAL")
print("=" * 55)

sin_ruido = esSinRuido(matriz_canal)
determinante = esDeterminante(matriz_canal)

print("¿Es un canal sin ruido?:", "SI" if sin_ruido else "NO")
print("¿Es un canal determinante?:", "SI" if determinante else "NO")

if sin_ruido and determinante:
    print("Clasificacion: sin ruido y determinante.")

elif sin_ruido:
    print("Clasificacion: sin ruido.")

elif determinante:
    print("Clasificacion: determinante.")

else:
    print("Clasificacion: ninguno de los dos.")


# ==================================================
# 12. METRICAS DEL CANAL
# ==================================================

print("\n")
print("=" * 55)
print("       C) METRICAS DEL CANAL")
print("=" * 55)

H_A = entropiaApriori(priori_probs)
H_B = entropiaSalida(priori_probs, matriz_canal)
H_A_B = equivocacion(priori_probs, matriz_canal)
H_B_A = perdida(priori_probs, matriz_canal)
H_AB = entropiaAfin(priori_probs, matriz_canal)
I_AB = informacionMutua(priori_probs, matriz_canal)

print(f"\nEntropia de entrada H(A):       {H_A:.4f} bits")
print(f"Entropia de salida H(B):        {H_B:.4f} bits")
print(f"Equivocacion H(A|B):            {H_A_B:.4f} bits")
print(f"Perdida H(B|A):                 {H_B_A:.4f} bits")
print(f"Entropia conjunta H(A,B):       {H_AB:.4f} bits")
print(f"Informacion mutua I(A;B):       {I_AB:.4f} bits")
print("Cumple relacion I(A,B) = H(A) - H(A|B) = H(B) - H(B|A):",
      "SI" if abs(I_AB - (H_A - H_A_B)) < 1e-9 and abs(I_AB - (H_B - H_B_A)) < 1e-9 else "NO")


# ==================================================
# 13. REDUCCION DEL CANAL
# ==================================================

print("\n")
print("=" * 55)
print("       D) REDUCCION DEL CANAL")
print("=" * 55)

matriz_reducida = reducirCanal(matriz_canal)

alfa_reducida = [
    "B" + str(i + 1)
    for i in range(len(matriz_reducida[0]))
]

imprimirMatriz(
    matriz_canal,
    alfa_entrada,
    alfa_salida,
    "MATRIZ DEL CANAL ORIGINAL",
    "Simbolos de entrada",
    "Simbolos de salida"
)

imprimirMatriz(
    matriz_reducida,
    alfa_entrada,
    alfa_reducida,
    "MATRIZ DEL CANAL REDUCIDO",
    "Simbolos de entrada",
    "Salidas reducidas"
)


# ==================================================
# 14. CAPACIDAD DEL CANAL
# ==================================================

print("\n")
print("=" * 55)
print("       E) CAPACIDAD DEL CANAL")
print("=" * 55)

paso = 0.001

capacidad, priori_optima = capacidadEstimada(
    matriz_reducida, paso
)

print(f"\nPaso utilizado: {paso}")
print(f"Capacidad estimada: {capacidad:.4f} bits")

print("\nProbabilidades a priori optimas:")

for i in range(len(priori_optima)):
    print(
        f"P({alfa_entrada[i]}) = "
        f"{priori_optima[i]:.4f}"
    )


# ==================================================
# 15. PROBABILIDAD DE ERROR
# ==================================================

print("\n")
print("=" * 55)
print("       F) PROBABILIDAD DE ERROR")
print("=" * 55)

# IMPORTANTE:
# Se usan los priors originales observados en la entrada,
# no los priors optimos calculados para la capacidad.

error = probabilidadError(
    priori_probs, matriz_reducida
)

print(f"\nProbabilidad de error minimo (MAP): {error:.4f}")

"""a. Las probabilidades a priori son frecuencias relativas de la entrada: P(a) = apariciones de a / total de simbolos. La matriz del canal sale de contar los pares (entrada, salida) en la misma posicion y dividir por las apariciones de cada entrada: P(b/a) = N(a,b) / N(a). Cada fila suma 1.
b. Es sin ruido si cada columna de la matriz tiene un solo valor distinto de 0 (cada salida viene de una sola entrada). Es determinante si cada fila tiene un solo valor distinto de 0 (cada entrada produce una sola salida). Se verifico sobre la matriz.
c. Primero P(b) = suma de P(a) * P(b/a) sobre todas las entradas, y P(a,b) = P(a) * P(b/a). Equivocacion H(A/B) = suma de P(b) * H(A/b): incertidumbre que queda sobre la entrada al ver la salida. Perdida H(B/A) = suma de P(a) * H(B/a): incertidumbre de la salida debida al ruido. Informacion mutua con su definicion: I(A,B) = suma de P(a,b) * log2( P(a,b) / (P(a) * P(b)) ). Se verifico que da lo mismo que H(A) - H(A/B) y que H(B) - H(B/A).
d. Se fusionan las columnas proporcionales: tienen las mismas probabilidades a posteriori, asi que la salida fusionada conserva toda la informacion sobre la entrada y la decision no cambia (reduccion suficiente). Se repite hasta que no queden columnas proporcionales y se verifica que las filas sumen 1 y que I(A,B) no cambie.
e. La capacidad C es el maximo de I(A,B) sobre todas las distribuciones de entrada. Se calculo sobre el canal reducido probando distribuciones con paso fijo y quedandose con la de mayor I. Para la probabilidad de error se uso el canal reducido y las a priori reales, con la regla MAP: a cada salida b se le asigna la entrada a* con mayor P(a/b), lo que equivale a comparar P(b/a) * P(a). Luego PE = suma de P(E/b) * P(b), con P(E/b) = 1 - P(a*/b). Es lo mismo que PE = 1 - suma de los maximos de cada columna de P(a,b).
f. La secuencia se ordeno en una matriz: cada fila es un caracter con su bit de paridad vertical a la derecha, y la primera fila es la paridad longitudinal. Se verifico la paridad de todas las filas y columnas, incluidos los bits de paridad. Si falla exactamente una fila y una columna, hay un error simple en su interseccion (dato o bit de paridad) y se corrige invirtiendolo. Si fallan solo filas, solo columnas o mas de una de cada una, hay mas de un error: se detecta pero no se corrige. Con los bits corregidos se reconstruye el mensaje, descartando la fila longitudinal y el bit vertical de cada caracter."""