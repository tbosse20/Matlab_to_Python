import matplotlib.pyplot as plt
import numpy as np

class Ball:
    resolution = 100

    def __init__(self, mass, radius, velocity, position, color, name, ax):
        self.mass = mass
        self.radius = radius
        self.velocity = velocity
        self.position = position
        self.color = color
        circle = self.make_circle()
        self.ball = plt.Polygon(circle, fill=self.color, edgecolor='k')
        if ax: ax.add_patch(self.ball)
        self.text = plt.text(
            self.position[0], self.position[1], name,
            horizontalalignment='center', verticalalignment='center',)

    def update_position(self, t):
        # Update circle with Python matplotlib: self.ball.center = self.position

        self.position = self.get_position_at_time_step(t).reshape((2, 1))
        circle = self.make_circle()
        self.ball.set_xy(circle)
        self.text.set_position(self.position)

    def get_position_at_time_step(self, dt):
        position = self.position.reshape((2, 1)) + dt * self.velocity.reshape((2, 1))
        return position.reshape((2, ))

    def make_circle(self):
        # Create circle in Python: matplotlib.patches.Circle(position, radius, color)

        t = np.linspace(0, 2 * np.pi, self.resolution)
        x_points = np.add(self.position[0], np.multiply(self.radius, np.cos(t)))
        y_points = self.position[1] + self.radius * np.sin(t)
        circle = np.stack((x_points, y_points), axis=1)
        return circle