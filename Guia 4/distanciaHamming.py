def distancia_hamming(u, v):
    d = 0
    for a, b in zip(u, v):
        if a != b:
            d += 1
    return d

def distancia_minima(codigo):
    dmin = len(codigo[0])
    for i in range(len(codigo)):
        for j in range(i + 1, len(codigo)):
            d = distancia_hamming(codigo[i], codigo[j])
            if d < dmin:
                dmin = d
    return dmin

def detecta_y_corrige(codigo):
    dmin = distancia_minima(codigo)
    return dmin, dmin - 1, (dmin - 1) // 2

codigo1 = ["0100100", "0101000", "0010010", "0100000"]
codigo2 = ["0100100", "0010010", "0101000", "0100001"]
codigo3 = ["0110000", "0000011", "0101101", "0100110"]

print(detecta_y_corrige(codigo1))   # (1, 0, 0)
print(detecta_y_corrige(codigo2))   # (2, 1, 0)
print(detecta_y_corrige(codigo3))   # (3, 2, 1)