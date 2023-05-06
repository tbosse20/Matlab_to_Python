import numpy as np
import matplotlib.pyplot as plt


class Ball:
    resolution = 100

    def __init__(self, mass, radius, velocity, position, color, name):
        self.mass = mass
        self.radius = radius
        self.velocity = velocity
        self.position = position
        self.color = color
        circle = self.make_circle()
        self.ball, = plt.plot(circle[0, :], circle[1, :], color=self.color)
        self.text = plt.text(self.position[0], self.position[1], name)

    def update_position(self, t):
        self.position = self.get_position_at_time_step(t)
        circle = self.make_circle()
        self.ball.set_xdata(circle[0, :])
        self.ball.set_ydata(circle[1, :])
        self.text.set_position(self.position)

    def get_position_at_time_step(self, dt):
        return self.position + dt * self.velocity

    def make_circle(self):
        t = np.linspace(0, 2 * np.pi, self.resolution)
        circle = np.vstack((self.position[0] + self.radius * np.cos(t),
                            self.position[1] + self.radius * np.sin(t)))
        return circle
