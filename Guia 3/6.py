def univocamente_decodificable(cod_bloque):
    if not no_singular(cod_bloque):
        #Si es singular la descartamos
        return False
    elif instantaneo(cod_bloque):
        #Si es instantaneo => Es UD
        return True
    else:
        #Sardinas-Patterson
        s_0 = set(cod_bloque)
        
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



def instantaneo(cod_bloque):
    for i in range(len(cod_bloque)):
        for j in range(i+1 , len(cod_bloque)):
            p1 = cod_bloque[i]
            p2 = cod_bloque[j]

            if p1.startswith(p2) or p2.startswith(p1):
                return False
    return True
#----------------------------------------------------------------
def no_singular(cod_bloque):
    return len(cod_bloque) == len(set(cod_bloque)) 
#Set elimina elementos duplicados

lenguage_codigo =[")", "[]", "]]", "([", "[()]", "([)]"]
if instantaneo(lenguage_codigo):
    print("Es instantaneo")
else:
    print("No es instantaneo")

if no_singular(lenguage_codigo):
    print("Es no singular")
else:
    print("Es singular")

if univocamente_decodificable(lenguage_codigo):
    print("Es univocamente decodificable")
else:
    print("No es univocamente decodificable")