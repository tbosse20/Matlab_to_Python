import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from newtons_method import *
from SuperPlanet import SuperPlanet

class Comet(SuperPlanet):
    # COMET Class. Uses the data from https://ssd.jpl.nasa.gov/sbdb.cgi?sstr = 1P
    coordinates = [0, 0]
    resolution = 200
    trace_length = 200

    def __init__(self, name, color, comet_data, ax):
        # Constructor
        self.name = name
        self.color = color
        self.radius = comet_data[0]
        self.a = comet_data[1]  # Halve storakse
        self.e = comet_data[2]  # Excentricitet
        self.M_0 = comet_data[3]
        self.t_0 = comet_data[4]
        self.n = comet_data[5]
        self.ax = ax

    def update(self, t):
        # Method for calculating the comets position at time t.
        if (t < -3000 or t > 3000): raise ('t must be in [-3000, 3000]')

        self.t = t

        # Convert t to the correct time relative
        # to the Julian Ephemeris Date:
        t = self.time_converter(t)
        # Calculate M from the available data
        M = self.M_0 + self.n * (t - self.t_0)
        M = self.mod_M(M)
        estar = 180 / np.pi * self.e
        # Calculate initial guess for Newtons method
        E_0 = M + estar * np.sin(M)
        # Apply Newtons method
        E = newtons_method(
            E_0, lambda E: E - estar * np.sin(np.deg2rad(E)) - M,
            lambda E: 1 - self.e * np.cos(np.deg2rad(E)), 1e-6)
        # Update coordinates
        self.coordinates = np.array([
            self.a * (np.cos(E) - self.e),
            self.a * np.sqrt(1 - self.e ** 2) * np.sin(E)
        ])
        if hasattr(self, "ball"):
            self.update_ball()
        else:
            self.make_ball()

    def time_converter(self, t):
        # Convert time t to Julian Ephemeris Date.
        t = (2816788 - 625674) * (t + 3001) / (3000 + 3001) + 625674
        return t