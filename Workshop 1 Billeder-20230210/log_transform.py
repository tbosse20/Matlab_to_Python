import numpy as np

def log_transform(A, c):
    # Denne funktion anvender intensitetstransformation
    # c * log(1 + a_ij) på matricen A. (Brug "numpy")

    return c * np.log(1 + A)

    raise ('Denne funktion er endnu ikke implementeret')
