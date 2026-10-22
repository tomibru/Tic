# s = alfabeto fuente
# c = codificacion de s, paralelas
def generar_bytearray(s,c, mensaje):
    bits = ""
    for letra in mensaje:
        for codigo, simbolo in zip(c,s):
            if(letra == simbolo):
                bits+= codigo
                break
    relleno = (-len(bits)) % 8
    bits += "0"*relleno

    ba = bytearray([relleno]) #Primer byte del array guarda la cantidad de relleno final
    for i in range(0, len(bits), 8):
        ba.append(int(bits[i: i+8],2))
    return ba

def decodificar_bytearray(s, c, ba):
    if len(ba) == 0 :
        return ""
    relleno = ba[0]

    bits =""
    for byte in ba[1:]:
        bits += format(byte, "08b")
    #Descarto relleno
    bits = bits[:len(bits) - relleno]

    tabla = dict(zip(c,s))

    mensaje = ""
    buffer = ""
    for bit in bits:
        buffer += bit
        if buffer in tabla:
            mensaje += tabla[buffer]
            buffer = ""

    return mensaje