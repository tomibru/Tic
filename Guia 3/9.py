import math
def obtener_alfabeto_codigo(palabras_codigo):
    alfabeto_codigo=""
    for palabra in palabras_codigo:
        for simbolo_codigo in palabra:
            if simbolo_codigo not in alfabeto_codigo:
                alfabeto_codigo += simbolo_codigo
    return alfabeto_codigo

    #Forma de una linea
    # 1. Unimos todas las palabras en una sola tira de texto
    # 2. set() elimina automáticamente los caracteres repetidos
    # 3. sorted() los ordena alfabéticamente/numéricamente
    # 4. "".join() une la lista ordenada de caracteres en una sola cadena
    # return "".join(sorted(set("".join(palabras_codigo))))

def obtener_longitud_palabras(palabras_codigo):
    longitud_palabras = []
    for palabra in palabras_codigo:
        longitud_palabras.append(len(palabra))
    return longitud_palabras

def inecuacion_kraft( alfabeto_codigo, longitud_palabras):
    r = len(alfabeto_codigo)
    suma = 0
    for longitud in longitud_palabras:
        suma += math.pow(r, -longitud)
    return (round(suma,10) <= 1)

palabras_codigo = [")", "[]", "]]", "([", "[()]", "([)]"];

alfabeto_codigo = obtener_alfabeto_codigo(palabras_codigo)
longitud_palabras = obtener_longitud_palabras(palabras_codigo)

print("---ALFABETO CODIGO---")

for simbolo in alfabeto_codigo:
    print(simbolo + " ")

print("---LONGITUD PALABRAS---")

for longitud in longitud_palabras:
    print(longitud)

if(inecuacion_kraft( alfabeto_codigo, longitud_palabras)):
    print("Cumple inecuacion de kraft")
else:
    print("No cumple inecuacion de kraft")