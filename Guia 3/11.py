import math

x = [")", "[]", "]]", "([", "[()]", "([)]"]
probs = [0.1,0.2,0.3,0.1,0.2,0.1]

def entropia(probs):
    return sum(-p * math.log2(p) for p in probs if p > 0)

def long_media(x, probs):
    return sum( probs[i] * len(x[i]) for i in range(len(x)))