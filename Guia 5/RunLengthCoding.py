def comprimir_rlc(mensaje):
    ba = bytearray()
    if len(mensaje) == 0:
        return ba

    actual = mensaje[0]
    cuenta = 1

    for letra in mensaje[1:]:
        if letra == actual and cuenta < 255:
            cuenta += 1
        else:
            ba.append(ord(actual))   # primer byte: ASCII del carácter
            ba.append(cuenta)        # segundo byte: cantidad de repeticiones
            actual = letra
            cuenta = 1

    # Cerrar la última ráfaga
    ba.append(ord(actual))
    ba.append(cuenta)

    return ba