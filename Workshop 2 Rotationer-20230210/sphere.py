import matplotlib.pyplot as plt
import numpy as np

# https://www.tutorialspoint.com/plotting-points-on-the-surface-of-a-sphere-in-python-s-matplotlib
def sphere():
    u, v = np.mgrid[0:2 * np.pi:21j, 0:np.pi:21j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    return [x, y, z]