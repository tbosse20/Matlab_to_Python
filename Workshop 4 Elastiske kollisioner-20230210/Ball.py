from matplotlib.patches import Circle
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
        # circle = self.make_circle()
        self.ball = Circle(position, radius=radius, color=color)
        if ax: ax.add_patch(self.ball)
        self.text = plt.text(self.position[0], self.position[1], name)

    def update_position(self, t):
        self.position = self.get_position_at_time_step(t).reshape((2, 1))
        self.ball.center = self.position
        self.text.set_position(self.position)

    def get_position_at_time_step(self, dt):
        print(f'{self.position=}')
        print(f'{self.velocity=}')
        position = self.position.reshape((2,)) + dt * self.velocity.reshape((2,))
        # print(position)
        return position.reshape((2, ))

    def make_circle(self):
        t = np.linspace(0, 2 * np.pi, self.resolution)
        v1 = np.add(self.position[0], np.multiply(self.radius, np.cos(t)))
        # v1 = np.multiply(self.radius, np.cos(t))
        v2 = self.position[1] + self.radius * np.sin(t)
        circle = np.vstack((v1, v2))
        return circle


if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import numpy as np

    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    ball1 = Ball(1.0, 0.20, np.array([0.0, 0.0], dtype=float), np.array([1, 2], dtype=float), 'r', 'Ball 1', ax)
    ball2 = Ball(0.5, 0.15, np.array([-0.01, -0.01], dtype=float), np.array([2, 2], dtype=float), 'b', 'Ball 2', ax)
    balls = [ball1, ball2]

    for i in range(100):
        for ball in balls:
            ball.update_position(i)
        plt.pause(0.001)
        fig.canvas.draw()
