import math

Lista = [0.5, 0.2, 0.15, 0.15]

# a. Cantidad de información de cada símbolo
def CrearListaInfo(Lista):
    ListaInfo = []
    for p in Lista:
        ListaInfo.append(-math.log2(p))
    return ListaInfo

# b. Entropía de la fuente
def entropia(Lista, ListaInfo):
    e = 0
    for i in range(len(Lista)):
        e = e + Lista[i] * ListaInfo[i]
    return e

ListaInfo = CrearListaInfo(Lista)

print("-----Cantidad de información-----\n", ListaInfo)
print("-----Entropía-----\n", entropia(Lista, ListaInfo))


