import numpy as np
import matplotlib.pyplot as plt
from newtons_method import newtons_method

class Planet:
    # PLANET Class. Based on the method of https://ssd.jpl.nasa.gov/txt/aprx_pos_planets.pdf

    t = 0  # Tid
    coordinates = np.array([0, 0])
    resolution = 200
    trace_length = 200

    def __init__(self, name, color, planet_data, ax):
        # Constructer
        self.name = name
        self.color = color
        self.radius = planet_data[0]
        self.a = planet_data[1]  # Halve storakse
        self.da = planet_data[2]  # Ændring i halve storakse pr. århundrede
        self.e = planet_data[3]  # Excentricitet
        self.de = planet_data[4]  # Ændring i excentricitet pr. århundrede
        self.L = planet_data[5]  # Middelbreddegrad
        self.dL = planet_data[6]  # Ændring i middelbreddegrad pr. århundrede
        self.baromega = planet_data[7]  # Breddegrad af periapsis
        self.dbaromega = planet_data[8]  # Ændring i breddegrad af periapsis pr. århundrede
        self.b = planet_data[9]  # Parameter
        self.c = planet_data[10]  # Parameter
        self.s = planet_data[11]  # Parameter
        self.f = planet_data[12]  # Parameter
        self.ax = ax

    def update(self, t):
        # Method for calculating the position of the planet at time t.
        if t < -3000 or t > 3000:
            raise ValueError("t must be in [-3000, 3000] for the model to be accurate")
        self.t = t
        # Convert t to the correct time relative to the Julian Ephemeris Date:
        t = self.time_converter(t)
        a = self.a + self.da * t
        e = self.e + self.de * t
        L = self.L + self.dL * t
        baromega = self.baromega + self.dbaromega * t
        # We calculate M from the available data
        M = L - baromega + self.b * t ** 2 + self.c * np.cos(np.deg2rad(self.f * t)) + self.s * np.sin(
            np.deg2rad(self.f * t))
        M = self.mod_M(M)
        estar = np.deg2rad(e)
        # Our initial guess in Newtons method
        E_0 = M + estar * np.sin(M)
        # We apply Newtons method to find E(t).
        E = newtons_method(E_0, lambda E: E - estar * np.sin(E) - M, lambda E: 1 - e * np.cos(E), 1e-6)
        # We calculate the coordinates of the planet at time t.
        self.coordinates = np.array([a * (np.cos(E) - e), a * np.sqrt(1 - e ** 2) * np.sin(E)])
        if hasattr(self, "ball"):
            self.update_planet()
        else:
            self.make_planet()

    def make_circle(self):
        t = np.linspace(0, 2 * np.pi, self.resolution)
        circle = self.radius * np.array([np.cos(t), np.sin(t)])
        circle += self.coordinates[:, np.newaxis]
        return circle.T

    def make_planet(self):
        circle = self.make_circle()
        self.ball = plt.Polygon(circle, color=self.color)
        if self.ax: self.ax.add_patch(self.ball)
        self.text = plt.text(self.coordinates[0], self.coordinates[1], self.name)
        trace = np.tile(self.coordinates[:, np.newaxis], (1, self.trace_length))
        self.trace, = plt.plot(trace[0], trace[1])

    def update_planet(self):
        circle = self.make_circle()
        self.ball.set_xy(circle)
        self.text.set_position(self.coordinates)
        trace_x = [self.coordinates[0], *self.trace.get_xdata()[:-1]]
        trace_y = [self.coordinates[1], *self.trace.get_ydata()[:-1]]
        self.trace.set_data(trace_x, trace_y)

    def time_converter(self, t):
        # Method for converting t to Julian Ephemeris Date and then to
        # centuries past J2000 .0.This is because of the available data.
        t = (2816788 - 625674) * (t + 3001) / (3000 + 3001) + 625674
        t = (t - 2451545) / 36525
        return t

    def mod_M(self, M):
        # Convert M to a value between - 180 deg and 180 deg.
        M = np.mod(M, 360) - 360 * (np.mod(M, 360) >= 180)
        return M