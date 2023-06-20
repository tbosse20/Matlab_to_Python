## Hjælpefunktioner

def sphere():
    # https://www.tutorialspoint.com/plotting-points-on-the-surface-of-a-sphere-in-python-s-matplotlib

    import matplotlib.pyplot as plt
    import numpy as np
    u, v = np.mgrid[0:2 * np.pi:21j, 0:np.pi:21j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    return [x, y, z]

def left_multiplication0(s, v):
    # Funktion der udregner matricen for venstre
    # multiplikation med kvatanionen [s, v]
    raise('Implementation mangler')

def right_multiplication0(s, v):
    # Funktion der udregner matricen for højre
    # multiplikation med kvatanionen [s, v]
    raise('Implementation mangler')

def left_multiplication(s, v):
    print(s, v)
    L = [
        [ s,     -v[0],  -v[1],  -v[2]],
        [v[0],     s,    -v[2],   v[1]],
        [v[1],    v[2],    s,    -v[0]],
        [v[2],   -v[1],   v[0],     s ]
    ]
    return L

def right_multiplication(s, v):
    R = [
        [ s,     -v[0],  -v[1],  -v[2]],
        [v[0],     s,     v[2],  -v[1]],
        [v[1],   -v[2],    s,     v[0]],
        [v[2],    v[1],  -v[0],     s ]
    ]
    return R