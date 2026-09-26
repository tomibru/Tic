probs = [0.2, 0.3, 0.1 , 0.4]
r = 2
import math
def entropia(probs):
    suma=0
    for p in probs:
        suma += p * -math.log(p,r)
    return suma