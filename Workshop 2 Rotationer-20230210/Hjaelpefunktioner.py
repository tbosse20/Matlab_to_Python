## Hjælpefunktioner
def left_multiplication2(s, v):
    # Funktion der udregner matricen for venstre
    # multiplikation med kvatanionen [s, v]
    raise('Implementation mangler')

def right_multiplication2(s, v):
    # Funktion der udregner matricen for højre
    # multiplikation med kvatanionen [s, v]
    raise('Implementation mangler')

def left_multiplication(s, v):
    L = [
        [ s,     -v(1),  -v(2),  -v(3)],
        [v(1),     s,    -v(3),   v(2)],
        [v(2),    v(3),    s,    -v(1)],
        [v(3),   -v(2),   v(1),     s ]
    ]
    return L

def right_multiplication(s, v):
    R = [
        [ s,     -v(1),  -v(2),  -v(3)],
        [v(1),     s,     v(3),  -v(2)],
        [v(2),   -v(3),    s,     v(1)],
        [v(3),    v(2),  -v(1),     s ]
    ]
    return R