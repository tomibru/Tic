import math

#15. Verificar si los códigos del ejercicio 8 son compactos y obtener conclusiones de acuerdo a los resultados obtenidos previamente.
def univocamente_decodificable(cod_bloque):
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

def obtener_alfabeto_codigo(palabras_codigo):
    alfabeto_codigo = ""
    for palabra in palabras_codigo:
        for simbolo_codigo in palabra:
            if simbolo_codigo not in alfabeto_codigo:
                alfabeto_codigo += simbolo_codigo
    return alfabeto_codigo


def compacto(codigos, probs):
    # 1. Obtenemos el alfabeto código a partir de la lista de códigos
    alfabeto_codigo = obtener_alfabeto_codigo(codigos)
    r = len(alfabeto_codigo)

    if univocamente_decodificable(codigos):
    # 3. Verificamos la longitud óptima de Shannon para cada palabra
        for i in range(len(codigos)):
            longitud_teorica = math.ceil(math.log(1 / probs[i], r))

            if len(codigos[i]) > longitud_teorica:
                return False
                
        return True
    else:
        return False

# --- Ejemplo de prueba (Fuente 1 binaria del Ejercicio 13) ---
# Distribución de probabilidades de la fuente (S1 a S6)
probs = [0.10, 0.50, 0.10, 0.20, 0.05, 0.05]

# Listas de palabras código para cada columna del Ejercicio 8
codigo_1 = ["==", "<", "<=", ">", ">=", "<>"]
codigo_2 = [")", "[]", "]]", "([", "[()]", "([)]"]
codigo_3 = ["/", "*", "-", "*", "++", "+-"]
codigo_4 = [ ".,", ";", ",,", ":", "...", ",:;"]

# Para probar el Código 1
print("Código 1 es compacto:", compacto(codigo_1, probs))

# Para probar el Código 2
print("Código 2 es compacto:", compacto(codigo_2, probs))

# Para probar el Código 3
print("Código 3 es compacto:", compacto(codigo_3, probs))

# Para probar el Código 4

print("Código 4 es UD:", univocamente_decodificable(codigo_4))
print("Alfabeto codigo", obtener_alfabeto_codigo(codigo_4))
print("Código 4 es compacto:", compacto(codigo_4, probs))

