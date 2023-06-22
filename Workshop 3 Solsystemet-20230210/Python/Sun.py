import numpy as np
from matplotlib import pyplot as plt


class Sun:
    name = 'Sun'
    coordinates = [0, 0]
    color = 'y'
    resolution = 500

    def __init__(self, r, ax):
        # Constructer
        self.radius = r
        self.create_sun(ax)

    def create_sun(self, ax):
        circle_points = self.make_circle()
        self.ball = plt.Polygon(circle_points, color=self.color)
        ax.add_patch(self.ball)
        self.text = plt.text(self.coordinates[0], self.coordinates[1], self.name)

    def make_circle(self):
        t = np.linspace(0, 2 * np.pi, self.resolution)
        circle_points = self.radius * np.array([np.cos(t), np.sin(t)]).T
        return circle_points

    def update(self):
        circle_points = self.make_circle()
        self.ball.set_xy(circle_points)
        self.ball.set_visible(False)
