import math

#"(]", "]", "[)", ")", "(["
#0.15, 0.25, 0.05, 0.45, 0.10
C = ["/", "*", "-", "*", "++", "+-"]
P = [0.10, 0.50, 0.10, 0.20, 0.05, 0.05]

def extraer_alfabeto_codigo(c):
    alfa = []
    for codigo in c:
        for simbolo in codigo:
            if simbolo not in alfa:
                alfa.append(simbolo)
    return sorted(alfa)

X = extraer_alfabeto_codigo(C)
print("---Alfabeto codigo---")
for simbolo in X:
    print(simbolo)
print("\n")


def entropia(x,probs):
    r = len(x)
    return sum(p * -math.log(p,r) for p in probs if p > 0)

print("---Entropia---")
print(entropia(X,P))
print("\n")


def longitud_media(probs,c):
    return sum(probs[i] * len(c[i]) for i in range(len(c)))

print("---Longitud media---")
print(longitud_media(P,C))
print("\n")

"""Inecuación de Kraft: Es la condición suficiente y necesaria para la existencia de 
al menos un código instantáneo con dichas longitudes"""

"""Inecuación de MacMillan:Si un código es UD, necesariamente satisface la inecuación."""

def inecuacion_kraft(c, x):
    r = len(x)
    return sum(r ** -len(codigo) for codigo in c)

print("---Inecuacion de Kraft---")
print(inecuacion_kraft(C,X))
print("\n")

"""Códigos No Singulares: Exigen que a cada símbolo fuente le corresponda una palabra código 
distinta. Evita confusiones al codificar símbolos individuales, pero no garantiza la 
decodificación de cadenas de símbolos concatenados"""
def no_singular(c):
    return len(c) == len(set(c)) 
#Set elimina elementos duplicados

print("---No singular---")
if no_singular(C):
    print("Es no singular")
else:
    print("Es singular")
print("\n")

"""Códigos Instantáneos (Libres de Prefijos): Exigen que ninguna palabra código 
coincida con el prefijo de otra. Permiten decodificar cada palabra en el momento 
exacto en que termina de recibirse, sin retardo ni necesidad de leer caracteres 
posteriores. Todo código instantáneo es automáticamente unívoco."""

def instantaneo(c):
    for i in range(len(c)):
        for j in range(i+1, len(c)):
            p1 = c[i]
            p2 = c[j]
            if p1.startswith(p2) or p2.startswith(p1):
                return False
    return True

print("---Instantaneo---")
if instantaneo(C):
    print("Es instantaneo")
else:
    print("No es instantaneo")
print("\n")

"""Códigos Unívocamente Decodificables (UD): Extienden la propiedad de no singularidad 
a cualquier extensión de orden $n$ ($n$ finito). Garantizan que cualquier secuencia de 
palabras concatenadas tenga una única lectura posible"""

def univocamente_decodificable(cod_bloque):
    if not no_singular(cod_bloque):
        #Si es singular la descartamos
        return False
    elif instantaneo(cod_bloque):
        #Si es instantaneo => Es UD
        return True
    else:
        #Sardinas-Patterson
        s_0 = set(cod_bloque)#Me deshago de los repetidos
        
        # 1. Armamos S1 (sufijos iniciales)
        s_k = set()
        for i in range(len(cod_bloque)):
            for j in range(i + 1, len(cod_bloque)):
                p1 = cod_bloque[i]
                p2 = cod_bloque[j]
                
                if p1.startswith(p2):
                    s_k.add(p1[len(p2):])  # p2 es prefijo de p1
                elif p2.startswith(p1):
                    s_k.add(p2[len(p1):])  # p1 es prefijo de p2

        # 2. Iteramos para generar S2, S3, ...
        s_historial = []  # Para detectar si entramos en un bucle infinito
        # isdisjoint : pregunta "¿estos dos conjuntos no tienen nada en común?"
        while s_k and s_k not in s_historial:
            # Si un sufijo en S_k es exactamente una palabra código original -> NO es UD
            if not s_k.isdisjoint(s_0):
                return False
            
            s_historial.append(s_k)
            
            # Generamos el siguiente conjunto S_(k+1)
            s_siguiente = set()
            for sufijo in s_k:
                for palabra in s_0:
                    if sufijo.startswith(palabra):
                        s_siguiente.add(sufijo[len(palabra):])
                    elif palabra.startswith(sufijo):
                        s_siguiente.add(palabra[len(sufijo):])
            
            s_k = s_siguiente

        return True

print("---Univocamente decodificable---")
if univocamente_decodificable(C):
    print("Es univocamente decodificable")
else:
    print("No es univocamente decodificable")
print("\n")


def compacto(x,codigos, probs):
    r = len(x)

    if univocamente_decodificable(codigos):
    # 2. Verificamos la longitud óptima de Shannon para cada palabra
        for i in range(len(codigos)):
            longitud_teorica = math.ceil(math.log(1 / probs[i], r))

            if len(codigos[i]) > longitud_teorica:
                return False
                
        return True
    else:
        return False

print("---Compacto---")
if compacto(X,C,P):
    print("Es compacto")
else:
    print("No es compacto")
print("\n")

def codigo_compacto_perfecto(X, C, P):
    return math.isclose(longitud_media(P,C), entropia(X,P), rel_tol=1e-9) and compacto(X,C,P)

print("---Codigo compacto perfecto---")
if codigo_compacto_perfecto(X, C, P):
    print("Es compacto perfecto\n ", entropia(X,P), " = " ,longitud_media(P,C))
else:
    print("No es compacto perfecto\n ", entropia(X,P), " != ", longitud_media(P,C))


