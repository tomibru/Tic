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