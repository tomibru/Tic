import random

def extraer_alfabeto_y_frecuencia(mensaje):
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

        for simbolo in frecuencias:
            alfabeto.append(simbolo)
            probabilidades.append(frecuencias[simbolo]/ totalChar)
        return alfabeto, probabilidades

def CrearMensaje(n, alfabeto, probabilidades):
    simulacion = random.choices(alfabeto, weights=probabilidades, k=n)
    mensajeGenerado = "".join(simulacion)

    return mensajeGenerado
   

#----A)
mensaje = "ABDAACAABACADAABDAADABDAAABDCDCDCDC"
alfa,probs= extraer_alfabeto_y_frecuencia(mensaje)
print(alfa, "    ", probs)

#----B)
n = 24
mensajeB = CrearMensaje(n, alfa, probs)
print("Cadena simulada ", mensajeB)





