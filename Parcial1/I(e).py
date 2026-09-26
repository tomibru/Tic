r = 2 #Base logaritmica
p = 0.5 #Probabilidad
import math
def cantidad_de_informacion(r, p):
    return -math.log(p,r)