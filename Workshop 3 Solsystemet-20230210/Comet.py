import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from newtons_method import *

class Comet:
    # COMET Class. Uses the data from https://ssd.jpl.nasa.gov/sbdb.cgi?sstr = 1P
    coordinates = [0, 0]
    resolution = 200
    trace_length = 200

    #da          # ændring i halve storakse pr. århundrede
    #de          # ændring i excentricitet pr. århundrede
    #t           # tid

    def __init__(self, name, color, comet_data):
        # Constructor
        if nargin > 0:
            self.name = name
            self.color = color
            self.radius = comet_data(1)
            self.a = comet_data(2)          # halve storakse
            self.e = comet_data(3)          # excentricitet
            self.M_0 = comet_data(4)
            self.t_0 = comet_data(5)
            self.n = comet_data(6)


    def time_converter(self, t):
        # Convert time t to Julian Ephemeris Date.
        t = (2816788 - 625674) * (t + 3001) / (3000 + 3001) + 625674
        return t

    def mod_M(self, M):
        # Convert M such that M is between -180 deg and 180 deg.
        M = np.mod(M, 360) - (np.mod(M, 360) >= 180) * 360
        return M

    def update_ball(self):
        circle = self.make_circle()
        # set(self.ball, 'XData', circle(1,:), 'YData', circle(2,:), 'Visible', 'off')
        # set(self.text, 'Position', [self.coordinates(1), self.coordinates(2)])
        # set(self.trace, 'XData', [self.coordinates(1), self.trace.XData(1: -1)], 'YData', [self.coordinates(2), self.trace.YData[1: -1]])
        # disp(self.trace.XData(1))
        return circle

    def update(self, t):
        # Method for calculating the comets position at time t.
        if (t < -3000 or t > 3000): raise ('t must be in [-3000, 3000]')

        self.t = t

        # Convert t to the correct time relative to the Julian Ephemeris
        # Date:
        t = self.time_converter(t)
        # Calculate M from the available data
        M = self.M_0 + self.n * (t - self.t_0)
        M = self.mod_M(M)
        estar = 180 / np.pi * self.e
        # Calculate initial guess for Newtons method
        E_0 = M + estar * sind(M)
        # Apply Newtons method
        E = newtons_method(E_0, @ (E) E - estar * np.sin(np.radians(E)) - M, @(E) 1 - self.e * cosd(E), 10 ^ (-6))
        # Update coordinates.
        self.coordinates = [self.a * (cosd(E) - self.e), self.a * np.sqrt(1 - self.e ^ 2) * sind(E)]
        '
        if not self.ball: self.make_ball()
        else: self.update_ball()

    def make_circle(self):
        t = np.linspace(0, 2 * np.pi, self.resolution)
        circle = self.coordinates + self.radius * [np.cos(t), np.sin(t)]
        return circle

    def make_ball(self):
        circle = self.make_circle()
        self.ball = patches.Patch(circle[1,:], circle[2,:], self.color, 'visible', 'off')
        self.text = plt.text(self.coordinates[1], self.coordinates[2], self.name)
        trace = self.coordinates * np.ones(2, self.trace_length)
        self.trace = plt.plot(trace[1, :], trace[2, :])
