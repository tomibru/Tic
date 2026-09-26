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