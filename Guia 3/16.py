import random
N = 8
codigos = ["A", "B", "C", "D"]
probs = [0.50, 0.25, 0.15, 0.10]


def generar_mensaje_aleatorio(codigos, probs, n):
    mensaje = ""
    for i in range(n):
        mensaje += random.choices(codigos, weights=probs)[0]
    return mensaje

print(generar_mensaje_aleatorio(codigos, probs, N))


