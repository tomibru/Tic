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

mensaje = "HOLA MUNDO ME VAN A DAR UN DIE EN TIC"
alfabeto = ["H", "O", "L", "A", " ", "M", "U", "N", "D", "E", "V", "R", "G", "T", "I", "C", "1", "0"]
codificacion = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111", "00000", "00001"]
print("Mensaje original:", mensaje)
ba = generar_bytearray(alfabeto, codificacion, mensaje)
print("Bytearray generado:", ba)
print("Mensaje decodificado:", decodificar_bytearray(alfabeto, codificacion, ba))