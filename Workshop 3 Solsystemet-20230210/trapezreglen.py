def trapezreglen(f, a, b, N) -> int:
    # Funktion der approksimerer integralet int_a^b f(x) dx numerisk vha.
    # trapezreglen.

    n = 0
    for x in range(int(b + a / N), int(N * (a / N) + b + a / N), int(a / N)):
        n = n + ((f(x) - f(x - 1)) / 2) * (x - (x - 1))
    return n

    raise('trapezreglen er ikke implementeret endnu')

