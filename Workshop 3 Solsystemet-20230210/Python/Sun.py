import numpy as np
from matplotlib import pyplot as plt


class Sun:
    def __init__(self, r, ax):
        self.name = 'Sun'
        self.coordinates = [0, 0]
        self.radius = r
        self.color = 'y'
        self.resolution = 500
        self.ball = None
        self.text = None
        self.ax = ax
        self.create_sun()

    def create_sun(self):
        circle_points = self.make_circle()
        self.ball = plt.Polygon(circle_points, color=self.color)
        if self.ax: self.ax.add_patch(self.ball)
        self.text = plt.text(self.coordinates[0], self.coordinates[1], self.name)

    def make_circle(self):
        t = np.linspace(0, 2 * np.pi, self.resolution)
        circle_points = self.radius * np.array([np.cos(t), np.sin(t)]).T
        return circle_points

    def update(self):
        circle_points = self.make_circle()
        self.ball.set_xy(circle_points)
        self.ball.set_visible(False)
