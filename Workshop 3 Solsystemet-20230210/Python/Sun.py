import numpy as np
from matplotlib import pyplot as plt
from SuperPlanet import SuperPlanet

class Sun(SuperPlanet):
    name = 'Sun'
    coordinates = [0, 0]
    color = 'y'
    resolution = 500

    def __init__(self, r, ax):
        # Constructer
        self.radius = r
        self.ax = ax
        self.make_ball()
