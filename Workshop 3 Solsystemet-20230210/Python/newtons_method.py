import numpy as np
def newtons_method(x0, f, f_prime, tol):
    x = x0
    while True:
        delta = f(x) / f_prime(x)
        x -= delta
        if np.abs(delta) < tol:
            break
    return x