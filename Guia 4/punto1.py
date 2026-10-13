
from math import log2, isclose


def primer_teorema_shannon(probabilidades, codigos, N):

    # Verificar que los datos sean validos
    if N < 1 or len(probabilidades) == 0:
        return False

    if len(codigos) != len(probabilidades) ** N:
        return False

    if any(p <= 0 or p > 1 for p in probabilidades):
        return False

    if not isclose(sum(probabilidades), 1.0):
        return False

    # Calcular la entropia de la fuente original
    H = -sum(p * log2(p) for p in probabilidades)

    # Calcular las probabilidades de la extension de orden N
    probabilidades_ext = []

    def generar_probabilidades(lista, prob_actual, nivel):
        if nivel == N:
            probabilidades_ext.append(prob_actual)
            return

        for p in lista:
            generar_probabilidades(
                lista, prob_actual * p, nivel + 1
            )

    generar_probabilidades(probabilidades, 1, 0)

    # Calcular la longitud media de la extension
    L_N = sum(
        p * len(codigo)
        for p, codigo in zip(probabilidades_ext, codigos)
    )

    # Verificar el Primer Teorema de Shannon
    return (
        H <= L_N / N + 1e-10
        and L_N / N < H + 1 / N
    )



# PUNTO 2
print("PUNTO 2")

probabilidades = [0.3, 0.1, 0.4, 0.2]
codigos = ["BA", "CAB", "A", "CBA"]
N = 1

resultado = primer_teorema_shannon(probabilidades, codigos, N)
print("Cumple Shannon:", resultado)


# PUNTO 3 - CODIFICACION C1
print("\nPUNTO 3 - C1")

probabilidades = [0.5, 0.2, 0.3]
codigos = ["11", "010", "00"]
N = 1

resultado = primer_teorema_shannon(probabilidades, codigos, N)
print("Cumple Shannon:", resultado)


# PUNTO 3 - CODIFICACION C2
print("\nPUNTO 3 - C2")

probabilidades = [0.5, 0.2, 0.3]
codigos = [
    "10", "001", "110", "010",
    "0000", "0001", "111", "0110", "0111"
]
N = 2

resultado = primer_teorema_shannon(probabilidades, codigos, N)
print("Cumple Shannon:", resultado)


# PUNTO 4
print("\nPUNTO 4")

probabilidades = [0.8, 0.2]

codigos = [
    "0",
    "100", "101", "110",
    "11100", "11101", "11110",
    "1111100"
]
N = 3

resultado = primer_teorema_shannon(probabilidades, codigos, N)
print("Cumple Shannon:", resultado)