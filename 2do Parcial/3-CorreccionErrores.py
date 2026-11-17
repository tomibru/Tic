# ============================================================
# DETECCIÓN Y CORRECCIÓN DE ERRORES CON PARIDAD VERTICAL,
# LONGITUDINAL Y CRUZADA
# ============================================================

entrada = "0100100001001001010000100001"

BITS_POR_FILA = 7      # 7 bits de dato + 1 bit de paridad vertical
PARIDAD = 0            # 0 = paridad par, 1 = paridad impar


def armar_matriz(mensaje, columnas):
    if len(mensaje) % columnas != 0:
        raise ValueError("El largo del mensaje no es múltiplo del ancho de fila.")
    return [
        [int(b) for b in mensaje[i:i + columnas]]
        for i in range(0, len(mensaje), columnas)
    ]


def paridad_ok(bits, paridad):
    # Con paridad par la suma total de bits debe ser par; con impar, impar.
    return sum(bits) % 2 == paridad


def filas_con_error(matriz, paridad):
    return [i for i, fila in enumerate(matriz) if not paridad_ok(fila, paridad)]


def columnas_con_error(matriz, paridad):
    errores = []
    for j in range(len(matriz[0])):
        columna = [matriz[i][j] for i in range(len(matriz))]
        if not paridad_ok(columna, paridad):
            errores.append(j)
    return errores


def corregir(matriz, paridad):
    filas = filas_con_error(matriz, paridad)
    columnas = columnas_con_error(matriz, paridad)

    if not filas and not columnas:
        return matriz, "Sin errores detectados.", None

    if len(filas) == 1 and len(columnas) == 1:
        i, j = filas[0], columnas[0]
        matriz[i][j] ^= 1
        return matriz, "Error simple detectado y corregido.", (i, j)

    return (
        matriz,
        "Errores detectados, pero no se pueden corregir (más de un error).",
        None,
    )


def matriz_a_texto(matriz):
    return "".join(str(b) for fila in matriz for b in fila)


def decodificar_ascii(matriz):
    # Paridad longitudinal arriba (se salta la primera fila)
    # y paridad vertical a la derecha (se descarta el último bit).
    caracteres = ""
    for fila in matriz[1:]:
        bits_dato = "".join(str(b) for b in fila[:-1])
        caracteres += chr(int(bits_dato, 2))
    return caracteres


# ------------------------------------------------------------
# Ejecución
# ------------------------------------------------------------

matriz = armar_matriz(entrada, BITS_POR_FILA)

print("Matriz recibida:")
for fila in matriz:
    print("".join(str(b) for b in fila))

print("\nFilas con error de paridad:", filas_con_error(matriz, PARIDAD))
print("Columnas con error de paridad:", columnas_con_error(matriz, PARIDAD))

matriz, estado, posicion = corregir(matriz, PARIDAD)

print("\n" + estado)
if posicion is not None:
    print(f"Posición corregida: fila {posicion[0] + 1}, columna {posicion[1] + 1}")

print("\nMatriz corregida:")
for fila in matriz:
    print("".join(str(b) for b in fila))

print("\nMensaje corregido:", matriz_a_texto(matriz))
print("Texto ASCII:", decodificar_ascii(matriz))
