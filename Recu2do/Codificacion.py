import math
alfabeto= ["A", "B", "C", "D"] #Supoción de alfabeto de la fuente
C = ["11", "01", "00", "10"]
mensaje_cod = "1100111001111001"

def extraer_probs(C, mensaje):
    frecuencias = [0] * len(C)
    longitud = len(C[0])

    for i in range(0, len(mensaje), longitud):
        simbolo = mensaje[i:i+longitud]

        if simbolo in C:
            posicion = C.index(simbolo)
            frecuencias[posicion] += 1

    total = sum(frecuencias)

    probabilidades = []

    for frecuencia in frecuencias:
        probabilidades.append(frecuencia / total)

    return probabilidades


print("\n")
print("-"*40)
print("Probabilidades de la fuente original:")
print("-"*40)
probs = extraer_probs(C, mensaje_cod)
print(C)
print(probs)

def entropia(probs):
    return -sum(p * math.log2(p) for p in probs if p > 0)

print("\n")
print("-"*40)
print("Entropía de la fuente original:")
print("-"*40)
print(entropia(probs))

def longitud_media(probabilidades, codigos):
    return sum(p * len(c) for p, c in zip(probabilidades, codigos))


def rendimiento_y_redundancia(probabilidades, codigos):
    H = entropia(probabilidades)
    L = longitud_media(probabilidades, codigos)

    rendimiento = H / L
    redundancia = 1 - rendimiento

    return rendimiento, redundancia

print("\n")
print("-"*40)
print("Rendimiento y Redundancia de la fuente codifi:")
print("-"*40)
rendimiento, redundancia = rendimiento_y_redundancia(probs, C)
print(f"Rendimiento: {rendimiento:.4f}")
print(f"Redundancia: {redundancia:.4f}")
print("\n")
print("-"*40)
print("Longitud media de la fuente codificada:")
print("-"*40)
L = longitud_media(probs, C)
print(f"Longitud media: {L:.4f}")


def huffman(probabilidades):
    items = [[p, ""] for p in probabilidades]

    if len(items) == 1:
        return ["0"]

    nodos = [[item[0], [item]] for item in items]

    while len(nodos) > 1:
        nodos.sort(key=lambda n: n[0])

        menor = nodos.pop(0)
        siguiente = nodos.pop(0)

        for item in menor[1]:
            item[1] = "0" + item[1]

        for item in siguiente[1]:
            item[1] = "1" + item[1]

        nodos.append([
            menor[0] + siguiente[0],
            menor[1] + siguiente[1]
        ])

    return [codigo for _, codigo in items]

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


# Generamos la extensión de orden n
extension, probabilidades_extension = extensionN(alfabeto, probs, 3)

H_extension = entropia(probabilidades_extension)

codigos_extension = huffman(probabilidades_extension)

L_extension = longitud_media(
    probabilidades_extension, codigos_extension
)

rendimiento_extension, redundancia_extension = (
    rendimiento_y_redundancia(
        probabilidades_extension, codigos_extension
    )
)

print("\n========================================")
print("       EXTENSIÓN DE ORDEN N")
print("========================================")

print("\nCantidad de símbolos:", len(extension))

print("\nProbabilidades y códigos:")

for simbolo, p, codigo in zip(
    extension, probabilidades_extension, codigos_extension
):
    print(f"{simbolo}\tP = {p:.6f}\tCódigo = {codigo}")

print(f"\nEntropía de la extensión: {H_extension:.4f} bits")
print("Longitud media:", round(L_extension, 4))
print("Rendimiento:", round(rendimiento_extension, 4))
print("Redundancia:", round(redundancia_extension, 4))


