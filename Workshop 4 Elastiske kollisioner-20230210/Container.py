import numpy as np
import matplotlib.pyplot as plt

class Container:
    def __init__(self, n):
        self.n = n
        x = np.linspace(0, 2*np.pi, n+1)
        self.vertices = np.vstack([np.cos(x), np.sin(x)])
        self.normals = self.normal_hat(self.vertices[:, 1:] - self.vertices[:, :-1])
        self.minx = np.min(self.vertices[0, :])
        self.maxx = np.max(self.vertices[0, :])
        self.miny = np.min(self.vertices[1, :])
        self.maxy = np.max(self.vertices[1, :])
        self.shape = plt.Polygon(self.vertices.T, fill=False, edgecolor='k')

    def in_container(self, x):
        return self.shape.contains_point(x.T)

    def normal_hat(self, x):
        return np.vstack([x[1, :], -x[0, :]]) / np.linalg.norm(x, axis=0)

    def reflect_edge(self, x, edge):
        if len(edge) != x.shape[1]:
            raise ValueError('Incompatible lengths')
        normals = self.normals[:, edge]
        return x - 2*np.sum(normals*x, axis=0)*normals

    def dist_to_boundary(self, x):
        m = x.shape[1]
        x = np.tile(x, (1, self.n))
        x_0 = np.tile(self.vertices[:, :-1], (m, 1)).T
        normals = np.tile(self.normals, (1, m))
        dist = np.sum(normals*(x-x_0), axis=0)
        idx = np.argmin(np.abs(dist))
        return dist[idx], idx

    def plot_container(self):
        plt.plot(self.vertices[0, :], self.vertices[1, :])
