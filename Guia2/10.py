import itertools #Preguntar
def punto10(alfabeto, probabilidades, n):
    probs_originales={}
    for i in range(len(alfabeto)):
        letra = alfabeto[i];
        probs_originales[letra]= probabilidades[i]

    combinaciones = list(itertools.product(alfabeto, repeat=n))
    alfaExt =[]
    probExt=[]

    for bloque in combinaciones:
        simboloExt = "".join(bloque)
        alfaExt.append(simboloExt)
        probAcumulada = 1.0
        for letra in bloque:
            probAcumulada= probAcumulada* probs_originales[letra];

        probExt.append(probAcumulada)

    return alfaExt, probExt
