def trapezreglen(f, a, b, N) -> int:
    # Funktion der approksimerer integralet int_a^b f(x) dx numerisk vha.
    # trapezreglen.
    # TODO: raise('trapezreglen er ikke implementeret endnu')

    n = 0
    for x in range(N + 1):
        t = a + (x / N) * (b - a)
        n = n + ((f(t) - f(t - 1 / N)) / 2) * (t - (t - 1 / N))
    return n


