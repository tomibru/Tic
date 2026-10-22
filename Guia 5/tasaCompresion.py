def tasa_compresion(mensaje, ba):
    if len(ba) == 0:
        return 0
    return len(mensaje) / len(ba)