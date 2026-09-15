import math

Lista = [0.5, 0.2, 0.15, 0.15]

# a. Cantidad de información de cada símbolo
def CrearListaInfo(Lista):
    for p in Lista:
        ListaInfo=[p] = -math.log2(Lista[p])
    return ListaInfo

# b. Entropía de la fuente
def entropia(Lista, ListaInfo):
    e = 0
    for i in range(len(Lista)):
        e = e + Lista[i] * ListaInfo[i]
    return e

ListaInfo = CrearListaInfo(Lista)

print("Cantidad de información:", ListaInfo)
print("Entropía:", entropia(Lista, ListaInfo))


