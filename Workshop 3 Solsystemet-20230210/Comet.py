import numpy as np
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from newtons_method import *


class Comet:
    # COMET Class. Uses the data from https://ssd.jpl.nasa.gov/sbdb.cgi?sstr = 1P
    coordinates = [0, 0]
    resolution = 200
    trace_length = 200

    # da          # ændring i halve storakse pr. århundrede
    # de          # ændring i excentricitet pr. århundrede
    # t           # tid

    def __init__(self, name, color, comet_data, ax):
        # Constructor
        nargin = 1  # TODO: What is this?
        if nargin > 0:
            self.name = name
            self.color = color
            self.radius = comet_data[0]
            self.a = comet_data[1]  # halve storakse
            self.e = comet_data[2]  # excentricitet
            self.M_0 = comet_data[3]
            self.t_0 = comet_data[4]
            self.n = comet_data[5]
            self.ax = ax

    def time_converter(self, t):
        # Convert time t to Julian Ephemeris Date.
        t = (2816788 - 625674) * (t + 3001) / (3000 + 3001) + 625674
        return t

    def mod_M(self, M):
        # Convert M such that M is between -180 deg and 180 deg.
        M = np.mod(M, 360) - (np.mod(M, 360) >= 180) * 360
        return M

    def update_ball(self):
        circle_points = self.make_circle()
        self.ball.set_xy(circle_points)
        # set(self.ball, 'XData', circle(1,:), 'YData', circle(2,:), 'Visible', 'off')
        # set(self.text, 'Position', [self.coordinates(1), self.coordinates(2)])
        # set(self.trace, 'XData', [self.coordinates(1), self.trace.XData(1: -1)], 'YData', [self.coordinates(2), self.trace.YData[1: -1]])
        # disp(self.trace.XData(1))

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
        E_0 = M + estar * np.sin(M)
        # Apply Newtons method
        E = newtons_method(
            E_0, lambda E: E - estar * np.sin(np.deg2rad(E)) - M,
            lambda E: 1 - self.e * np.cos(np.deg2rad(E)), 1e-6)
        # Update coordinates.
        self.coordinates = [
            self.a * (np.cos(E) - self.e),
            self.a * np.sqrt(1 - self.e ** 2) * np.sin(E)
        ]
        if hasattr(self, "ball"):
            self.update_ball()
        else:
            self.make_ball()

    def make_circle(self):
        # Create circle in Python: matplotlib.patches.Circle(position, radius, color)

        t = np.linspace(0, 2 * np.pi, self.resolution)
        x_points = np.add(self.coordinates[0], np.multiply(self.radius, np.cos(t)))
        y_points = self.coordinates[1] + self.radius * np.sin(t)
        circle_points = np.stack((x_points, y_points), axis=1)
        return circle_points

    def make_ball(self):
        circle_points = self.make_circle()
        # TODO: Compare circle with original
        self.ball = plt.Polygon(circle_points, self.color)
        self.ax.add_patch(self.ball)
        self.text = plt.text(self.coordinates[0], self.coordinates[1], self.name)
        trace = np.multiply(np.transpose([self.coordinates]), np.ones((2, self.trace_length)))
        self.trace = plt.plot(trace[0, :], trace[1, :])
