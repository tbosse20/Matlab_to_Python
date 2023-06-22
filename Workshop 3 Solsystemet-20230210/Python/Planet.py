import numpy as np
import matplotlib.pyplot as plt

class Planet:
    def __init__(self, name, color, planet_data, ax):
        self.name = name
        self.color = color
        self.radius = planet_data[0]
        self.coordinates = np.array([0, 0])
        self.resolution = 200
        self.a = planet_data[1]
        self.da = planet_data[2]
        self.e = planet_data[3]
        self.de = planet_data[4]
        self.L = planet_data[5]
        self.dL = planet_data[6]
        self.baromega = planet_data[7]
        self.dbaromega = planet_data[8]
        self.t = 0
        self.b = planet_data[9]
        self.c = planet_data[10]
        self.s = planet_data[11]
        self.f = planet_data[12]
        self.trace = None
        self.trace_length = 200
        self.ball = None
        self.text = None
        self.ax = ax

    def update(self, t):
        if t < -3000 or t > 3000:
            raise ValueError("t must be in [-3000, 3000] for the model to be accurate")
        self.t = t
        t = self.time_converter(t)
        a = self.a + self.da * t
        e = self.e + self.de * t
        L = self.L + self.dL * t
        baromega = self.baromega + self.dbaromega * t
        M = L - baromega + self.b * t**2 + self.c * np.cos(np.deg2rad(self.f * t)) + self.s * np.sin(np.deg2rad(self.f * t))
        M = self.mod_M(M)
        estar = np.deg2rad(e)
        E_0 = M + estar * np.sin(M)
        E = self.newtons_method(E_0, lambda E: E - estar * np.sin(E) - M, lambda E: 1 - e * np.cos(E), 1e-6)
        self.coordinates = np.array([a * (np.cos(E) - e), a * np.sqrt(1 - e**2) * np.sin(E)])
        if self.ball is None:
            self.make_planet()
        else:
            self.update_planet()

    def make_circle(self):
        t = np.linspace(0, 2 * np.pi, self.resolution)
        circle = self.coordinates[:, np.newaxis] + self.radius * np.array([np.cos(t), np.sin(t)])
        return circle

    def make_planet(self):
        circle = self.make_circle()
        self.ball = plt.Polygon(circle.T, color=self.color, visible=False)
        self.ax.add_patch(self.ball)
        self.text = plt.text(self.coordinates[0], self.coordinates[1], self.name)
        trace = np.tile(self.coordinates[:, np.newaxis], (1, self.trace_length))
        self.trace, = plt.plot(trace[0], trace[1])

    def update_planet(self):
        circle = self.make_circle()
        self.ball.set_xy(circle.T)
        self.ball.set_visible(False)
        self.text.set_position(self.coordinates)
        self.trace.set_data([self.coordinates[0], *self.trace.get_xdata()[:-1]], [self.coordinates[1], *self.trace.get_ydata()[:-1]])

    def time_converter(self, t):
        t = (2816788 - 625674) * (t + 3001) / (3000 + 3001) + 625674
        t = (t - 2451545) / 36525
        return t

    def mod_M(self, M):
        M = np.mod(M, 360) - 360 * (np.mod(M, 360) >= 180)
        return M

    @staticmethod
    def newtons_method(x0, f, f_prime, tol):
        x = x0
        while True:
            delta = f(x) / f_prime(x)
            x -= delta
            if np.abs(delta) < tol:
                break
        return x
