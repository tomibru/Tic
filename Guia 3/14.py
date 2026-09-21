import math

def obtener_alfabeto_codigo(palabras_codigo):
    alfabeto_codigo = ""
    for palabra in palabras_codigo:
        for simbolo_codigo in palabra:
            if simbolo_codigo not in alfabeto_codigo:
                alfabeto_codigo += simbolo_codigo
    return alfabeto_codigo

def inecuacion_kraft(alfabeto_codigo, codigos):
    r = len(alfabeto_codigo)
    # Sumatoria de Kraft: sum(r ** -len(c)) <= 1
    return sum(r ** -len(codigo) for codigo in codigos) <= 1

def compacto(codigos, probs):
    # 1. Obtenemos el alfabeto código a partir de la lista de códigos
    alfabeto_codigo = obtener_alfabeto_codigo(codigos)
    r = len(alfabeto_codigo)
    
    # 2. Verificamos la inecuación de Kraft
    if not inecuacion_kraft(alfabeto_codigo, codigos):
        return False
    
    # 3. Verificamos la longitud óptima de Shannon para cada palabra
    for i in range(len(codigos)):
        longitud_teorica = math.ceil(math.log(1 / probs[i], r))
        if len(codigos[i]) != longitud_teorica:
            return False
            
    return True

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
print("Código 4 es compacto:", compacto(codigo_4, probs))