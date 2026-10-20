def generar_combinaciones(alfabeto, n):
    combinaciones = [""]  # arranca con el bloque vacío

    for _ in range(n):
        nuevas_combinaciones = []
        for bloque in combinaciones:
            for letra in alfabeto:
                nuevas_combinaciones.append(bloque + letra)
        combinaciones = nuevas_combinaciones

    return combinaciones


def punto10(alfabeto, probabilidades, n):
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

alfabeto = ['A', 'B', 'C']
probabilidades = [0.5, 0.3, 0.2]
n = 2

alfaExt, probExt = punto10(alfabeto, probabilidades, n)

print(f"Alfabeto original: {alfabeto}")
print(f"Probabilidades originales: {probabilidades}")
print(f"Orden de extensión n = {n}\n")

print("Alfabeto extendido y sus probabilidades:")
for simbolo, prob in zip(alfaExt, probExt):
    print(f"  {simbolo} -> {prob:.4f}")

print(f"\nCantidad de símbolos extendidos: {len(alfaExt)}")
print(f"Suma de probabilidades: {sum(probExt):.6f}  (debe dar 1.0)")


"""Conclusiones 1:

Ambos mensajes tienen probabilidades marginales parecidas, cerca de 0.25 por símbolo, y la 
entropía de orden cero es casi la máxima (≈2 bits). Solo con eso no se puede saber si hay
memoria.
Al mirar la matriz, en el Mensaje 2 las condicionales están lejísimos de las marginales. 
Por ejemplo, tras + viene * con probabilidad 1. Por eso la entropía cae de 2.00 a 
0.46: conocer el símbolo anterior quita casi toda la incertidumbre.
El vector estacionario se parece a las marginales, y eso es esperable.
En el Mensaje 1 la tolerancia decide la clasificación, así que hay que justificarla.

"""


"""Conclusiones 2:

A y B tienen las mismas longitudes, por lo que tienen igual L y Kraft = 1.
A es instantáneo, por lo tanto UD, no singular y compacto.
B cumple Kraft pero no es UD, y eso muestra que Kraft solo garantiza que existe un 
código instantáneo con esas longitudes, no que el elegido lo sea.

Consejos para redactar
Citá siempre tus valores concretos (entropías, diferencia máxima, tolerancia).
Declará la tolerancia que usaste para decidir la memoria.
Evitá frases como "los resultados fueron los esperados": no suman puntos por sí solas. 
Es mejor decir por qué eran los esperados.

"""