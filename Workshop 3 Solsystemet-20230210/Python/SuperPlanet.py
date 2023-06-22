import numpy as np
from matplotlib import pyplot as plt


class SuperPlanet:
    coordinates = None
    resolution = None
    radius = None
    ax = None

    def make_circle(self):
        # Create circle in Python: matplotlib.patches.Circle(position, radius, color)

        t = np.linspace(0, 2 * np.pi, self.resolution)
        x_points = np.add(self.coordinates[0], np.multiply(self.radius, np.cos(t)))
        y_points = self.coordinates[1] + self.radius * np.sin(t)
        circle_points = np.stack((x_points, y_points), axis=1)
        return circle_points

    def make_ball(self):
        circle_points = self.make_circle()
        self.ball = plt.Polygon(circle_points, color=self.color)
        if self.ax: self.ax.add_patch(self.ball)
        self.text = plt.text(self.coordinates[0], self.coordinates[1], self.name)
        if hasattr(self, 'trace_length'):
            trace = np.tile(self.coordinates[:, np.newaxis], (1, self.trace_length))
            self.trace, = plt.plot(trace[0], trace[1])

    def update_ball(self):
        circle_points = self.make_circle()
        self.ball.set_xy(circle_points)
        self.text.set_position(self.coordinates)
        if hasattr(self, 'trace_length'):
            trace_x = [self.coordinates[0], *self.trace.get_xdata()[:-1]]
            trace_y = [self.coordinates[1], *self.trace.get_ydata()[:-1]]
            self.trace.set_data(trace_x, trace_y)

    def mod_M(self, M):
        # Convert M to a value between - 180 deg and 180 deg.
        M = np.mod(M, 360) - 360 * (np.mod(M, 360) >= 180)
        return M
