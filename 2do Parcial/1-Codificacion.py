
from math import log2, ceil


# ============================================================
# 1. DATOS DE LA FUENTE
# ============================================================

mensaje = "GIIHGGGHGIHHIHIIGFHH"


# ============================================================
# 2. FUNCIONES GENERALES
# ============================================================

def extraer_alfabeto_y_probabilidades(mensaje):
    frecuencias = {}
    total = len(mensaje)

    if total == 0:
        return [], []

    for simbolo in mensaje:
        if simbolo in frecuencias:
            frecuencias[simbolo] += 1
        else:
            frecuencias[simbolo] = 1

    alfabeto = sorted(frecuencias.keys())
    probabilidades = [frecuencias[s] / total for s in alfabeto]

    return alfabeto, probabilidades


def entropia(probabilidades):
    return -sum(p * log2(p) for p in probabilidades if p > 0)


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


def longitud_media(probabilidades, codigos):
    return sum(p * len(c) for p, c in zip(probabilidades, codigos))


def rendimiento_y_redundancia(probabilidades, codigos):
    H = entropia(probabilidades)
    L = longitud_media(probabilidades, codigos)

    rendimiento = H / L
    redundancia = 1 - rendimiento

    return rendimiento, redundancia


def generar_diccionario(alfabeto, codigos):
    return dict(zip(alfabeto, codigos))


def imprimir_codigo(alfabeto, probabilidades, codigos):
    print("Símbolo\tProbabilidad\tCódigo")

    for simbolo, p, codigo in zip(alfabeto, probabilidades, codigos):
        print(f"{simbolo}\t{p:.4f}\t\t{codigo}")


def verificar_shannon(H, L):
    return H <= L < H + 1


# ============================================================
# 3. CÓDIGO PARA LA FUENTE ORIGINAL
# ============================================================

alfabeto, probabilidades = extraer_alfabeto_y_probabilidades(mensaje)

H = entropia(probabilidades)
codigos = huffman(probabilidades)

diccionario = generar_diccionario(alfabeto, codigos)

mensaje_codificado = ''.join(diccionario[s] for s in mensaje)

L = longitud_media(probabilidades, codigos)
rendimiento, redundancia = rendimiento_y_redundancia(
    probabilidades, codigos
)

# Cada carácter del mensaje original ocupa 8 bits (ASCII).
bits_originales = len(mensaje) * 8
bits_codificados = len(mensaje_codificado)

tasa_compresion = bits_originales / bits_codificados


print("\n========================================")
print("       CÓDIGO PARA LA FUENTE")
print("========================================")

print("\nMensaje original:", mensaje)
print("Cantidad de símbolos:", len(mensaje))
print("Alfabeto:", alfabeto)

print("\nProbabilidades:")
for simbolo, p in zip(alfabeto, probabilidades):
    print(f"P({simbolo}) = {p:.4f}")

print(f"\nEntropía de la fuente: {H:.4f} bits")

print("\nCódigo de Huffman:")
imprimir_codigo(alfabeto, probabilidades, codigos)

print("\nMensaje codificado:")
print(mensaje_codificado)

print("\nTasa de compresión:")
print(f"{tasa_compresion:.4f}:1")

print("\nLongitud media:", round(L, 4))
print("Rendimiento:", round(rendimiento, 4))
print("Redundancia:", round(redundancia, 4))

print("\nPrimer Teorema de Shannon:")
if verificar_shannon(H, L):
    print("La fuente CUMPLE.")
else:
    print("La fuente NO CUMPLE.")



# ============================================================
# 4. GENERAR LA EXTENSIÓN DE ORDEN 3
# ============================================================

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


# Generamos la extensión de orden 3
extension, probabilidades_extension = extensionN(alfabeto, probabilidades, 3)


# ============================================================
# 5. CÓDIGO PARA LA EXTENSIÓN
# ============================================================

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
print("       EXTENSIÓN DE ORDEN 3")
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

print("\nLongitud media por símbolo original:")
print(round(L_extension / 3, 4))

print("\nPrimer Teorema de Shannon:")
if verificar_shannon(H_extension, L_extension):
    print("La extensión CUMPLE.")
else:
    print("La extensión NO CUMPLE.")


# ============================================================
# 6. COMPARACIÓN DE LOS DOS CÓDIGOS
# ============================================================

print("\n========================================")
print("             COMPARACIÓN")
print("========================================")

print(f"Fuente:     L = {L:.4f} | Rendimiento = {rendimiento:.4f} | Redundancia = {redundancia:.4f}")

print(f"Extensión:  L = {L_extension:.4f} | Rendimiento = {rendimiento_extension:.4f} | Redundancia = {redundancia_extension:.4f}")

print(f"\nFuente: {L:.4f} bits por símbolo")
print(f"Extensión: {L_extension / 3:.4f} bits por símbolo original")


"""**Análisis y conclusiones**

Al comparar ambos códigos, observamos que la extensión de orden 3 obtiene un mayor rendimiento (0.9966 frente a 0.8942) y una menor redundancia (0.0034 frente a 0.1058).
Esto se debe a que, al agrupar los símbolos de la fuente de a tres y aplicar un algoritmo de codificación óptima como Huffman, se obtiene una longitud media por símbolo más cercana a la entropía de la fuente.
Según el Primer Teorema de Shannon, la entropía establece un límite inferior para la longitud media de un código binario sin pérdida de información. A medida que aumenta el orden de la extensión, la longitud media por símbolo puede aproximarse cada vez más a ese límite.
Por lo tanto, la extensión permite construir un código más compacto, aprovechando mejor las probabilidades de los símbolos y reduciendo la redundancia. En este caso, el rendimiento de 0.9966 indica que la longitud media obtenida está muy próxima al límite teórico de Shannon.
Sin embargo, aumentar el orden de la extensión también incrementa el tamaño del alfabeto y la complejidad de la codificación.
"""

"""
a. Probabilidades como frecuencias relativas: P(sᵢ) = apariciones / total, con P(1) = 0,625 y P(0) = 0,375. Entropía: H = −Σ P·log₂P = 0,9544 bits/símbolo.
b. Se aplicó Huffman (código compacto): se unen sucesivamente los dos símbolos menos probables sumando sus probabilidades, y el código sale de recorrer el árbol. Quedan 0 y 1.
c. Tasa = tamaño original / tamaño codificado. Con ASCII (8 bits/carácter): 128 / 16 = 8:1.
d. Se generó S³ (8 bloques), con probabilidad de cada bloque igual al producto de las de sus símbolos (fuente sin memoria), y se aplicó Huffman sobre ellas, con longitudes de 2 a 4 bits.
e. L = Σ P·l, η = H/L, R = 1 - η. Fuente: L = 1, η = 0,9544, R = 0,0456. Extensión: L₃ = 2,8965 (0,9655 por símbolo), η = 2,8632/2,8965 = 0,9885, R = 0,0115.
f. Se verifica H(S) ≤ Lₙ/n < H(S) + 1/n con el código generado. Fuente: 0,9544 ≤ 1 < 1,9544, cumple. Extensión: 0,9544 ≤ 0,9655 < 1,2877, cumple.
"""

"""“
La longitud media de la extensión (Lₙ) parece mayor que la de la fuente porque está expresada 
en bits por bloque de n símbolos, mientras que la de la fuente está en bits por símbolo. 
Para compararlas se normaliza: Lₙ/n da los bits por símbolo original, y ese valor resulta 
menor que L y más cercano a la entropía.

Ambos códigos son compactos (Huffman) y cumplen el Primer Teorema de Shannon: 
H(S) ≤ Lₙ/n < H(S) + 1/n. Como la cota superior decrece con 1/n, la extensión acerca la 
longitud media por símbolo a la entropía, lo que se refleja en un mayor rendimiento y una 
menor redundancia. Esto ocurre porque el código por símbolo debe usar una cantidad entera de 
bits y desperdicia la diferencia con la entropía, mientras que al codificar bloques ese redondeo 
se reparte entre los n símbolos.
La mejora tiene un costo: el alfabeto crece exponencialmente (qⁿ palabras código), lo que 
implica mayor complejidad de construcción, codificación y decodificación, mayor demora al tener que
esperar un bloque completo, y la necesidad de completar el mensaje cuando su largo no es múltiplo de n. 
Además, la ganancia es decreciente al aumentar n, por lo que conviene elegir un n que equilibre rendimiento y complejidad.
La tasa de compresión se debe a pasar de la representación original (por ejemplo, 8 bits por 
carácter en ASCII) a una longitud media cercana a la entropía de la fuente.
”"""