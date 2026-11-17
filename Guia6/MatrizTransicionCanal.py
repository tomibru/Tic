def extraer_alfabeto(c):
    alfa = []
    for simbolo in c:
        if simbolo not in alfa:
            alfa.append(simbolo)
    return sorted(alfa)

def extraer_priori(entrada):
    alfa_entrada = extraer_alfabeto(entrada)
    contador_entrada = {}
    for simbolo in alfa_entrada:
        contador_entrada[simbolo] = 0
    for letra in entrada:
        contador_entrada[letra] += 1
    probs_priori = []
    for letra in alfa_entrada:
        probs_priori.append(contador_entrada[letra] / len(entrada))
        
    print("\nPROBABILIDADES A PRIORI")
    for i in range(len(alfa_entrada)):
        print(f"P({alfa_entrada[i]}) = {probs_priori[i]:.4f}")

    return probs_priori 
        

def matrizCanal(entrada, salida):
    alfa_entrada = extraer_alfabeto(entrada)
    alfa_salida = extraer_alfabeto(salida)

    contador_entrada = {}
    for simbolo in alfa_entrada:
        contador_entrada[simbolo] = 0
    for letra in entrada:
        contador_entrada[letra] += 1

    matriz = []
    for i in range(len(alfa_entrada)):
        fila = []
        for j in range(len(alfa_salida)):
            fila.append(0)
        matriz.append(fila)

    for i in range(len(entrada)):
        simboloE = entrada[i]
        simboloS = salida[i]

        fila = alfa_entrada.index(simboloE)
        col = alfa_salida.index(simboloS)

        matriz[fila][col] += 1

    for i in range(len(alfa_entrada)):
        for j in range(len(alfa_salida)):
            matriz[i][j] = matriz[i][j] / contador_entrada[alfa_entrada[i]] 

    return matriz

def imprimirMatriz(matriz, alfa_entrada, alfa_salida):
    print("\nMATRIZ DEL CANAL")
    print("Filas: símbolos de entrada")
    print("Columnas: símbolos de salida\n")

    print(f"{'Entrada/Salida':<18}", end="")
    for simbolo in alfa_salida:
        print(f"{simbolo:>10}", end="")
    print()

    for i in range(len(alfa_entrada)):
        print(f"{alfa_entrada[i]:<18}", end="")
        for j in range(len(alfa_salida)):
            print(f"{matriz[i][j]:>10.4f}", end="")
        print()

entrada = "abcacaabbcacaabcacaaabcaca"
salida = "01010110011001000100010011"
probs_a_priori = extraer_priori(entrada)
matriz_canal = matrizCanal(entrada, salida)
imprimirMatriz(matriz_canal, extraer_alfabeto(entrada), extraer_alfabeto(salida))


    