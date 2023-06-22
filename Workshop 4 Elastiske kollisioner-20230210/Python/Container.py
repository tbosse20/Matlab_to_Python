import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath


class Container:
    def __init__(self, n, ax):
        self.n = n
        x = np.linspace(0, 2 * np.pi, n + 1)
        self.vertices = np.vstack([np.cos(x), np.sin(x)])
        self.normals = self.normal_hat(self.vertices[:, 1:] - self.vertices[:, :-1])
        self.minx = np.min(self.vertices[0, :])
        self.maxx = np.max(self.vertices[0, :])
        self.miny = np.min(self.vertices[1, :])
        self.maxy = np.max(self.vertices[1, :])
        self.shape = plt.Polygon(self.vertices.T, fill=False, edgecolor='k')
        if ax: ax.add_patch(self.shape)

    def in_container(self, x):
        x, y, vertices_x, vertices_y = x[0, :], x[1, :], self.vertices[0, :], self.vertices[1, :]
        vertices = np.column_stack((vertices_x, vertices_y))
        path = mplPath.Path(vertices)
        return path.contains_points(np.column_stack((x, y))).astype(int)

    def normal_hat(self, x):
        return np.vstack([x[1, :], -x[0, :]]) / np.linalg.norm(x, axis=0)

    def reflect_edge(self, velocity, edge):
        normals = self.normals[:, edge]
        reflection = 2 * np.dot(normals.T, velocity)[0] * normals
        reflected_vec = velocity - reflection.reshape(2, 1)
        return reflected_vec

    def dist_to_boundary(self, position):
        m = 1
        position = np.tile(position, (1, self.n))
        x_0 = np.tile(self.vertices[:, :-1], (m, 1))
        normals = np.tile(self.normals, (1, m))
        dist = np.sum(normals * (position - x_0), axis=0)
        idx = np.argmin(np.abs(dist))
        return dist, idx

    def plot_container(self):
        plt.plot(self.vertices[0, :], self.vertices[1, :])