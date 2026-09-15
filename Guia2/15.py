#Inciso a
def inicializarMatriz(n):
    matriz = []
    for i in range(n):
        fila =[]
        for j in range(n):
            fila.append(0)
        matriz.append(fila)
    return matriz
        

def incisoA(cadena):
    contSimbolos ={}
    for letra in cadena:
        if letra in contSimbolos:
            contSimbolos[letra] = contSimbolos[letra] + 1
        else:
            contSimbolos[letra] = 1

    transiciones = {}
    salidas={}
    for i in range(len(cadena)-1):
        actual = cadena[i]
        siguiente = cadena[i+1]

        if actual in salidas:
            salidas[actual] += 1
        else:
            salidas[actual] = 1

        if (actual , siguiente) in transiciones:
            transiciones[(actual , siguiente)] += 1
        else:
            transiciones[(actual , siguiente)] = 1

    M = inicializarMatriz(len(contSimbolos))

    alfabeto = list(contSimbolos.keys())
    

    for transicion in transiciones:
        actual = transicion[0]
        siguiente = transicion[1]

        fila = alfabeto.index(siguiente)
        columna = alfabeto.index(actual)

        M[fila][columna] = transiciones[transicion] / salidas[actual]

    return alfabeto ,M

cadena = input("Ingrese el mensaje: ")

alfabeto, M = incisoA(cadena)

print("Alfabeto:", alfabeto)
print("Matriz de transición:")

for fila in M:
    print(fila)

#Inciso b
import random
def retornarCadena(n,alfabeto,transicion):
    cadena = []

    #Simbolo inicial al azar
    simbolo = random.choice(alfabeto)
    cadena.append(simbolo)

    while len(cadena) < n: 
        columna = alfabeto.index(simbolo)
        probabilidades = []
        for i in range(len(alfabeto)):
            probabilidades.append(transicion[i][columna])
        simbolo = random.choices(alfabeto, weights = probabilidades)

        cadena.append(simbolo)
    return cadena



