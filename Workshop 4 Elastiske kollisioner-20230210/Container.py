import numpy as np
import matplotlib.pyplot as plt

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

        import matplotlib.path as mplPath

        x, y, vertices_x, vertices_y = x[0, :], x[1, :], self.vertices[0, :], self.vertices[1, :]
        vertices = np.column_stack((vertices_x, vertices_y))
        path = mplPath.Path(vertices)
        return path.contains_points(np.column_stack((x, y))).astype(int)

        return self.shape.contains_point(x)

    def normal_hat(self, x):
        return np.vstack([x[1, :], -x[0, :]]) / np.linalg.norm(x, axis=0)

    def reflect_edge(self, velocity, edge):
        if edge.size != velocity.shape[1]:
            raise ValueError('Incompatible lengths')
        normals = self.normals[:, edge]
        return velocity - 2 * np.sum(normals * velocity, axis=0)*normals

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

if __name__ == '__main__':
    container = Container(4, None)
    position = np.array([0.6, 0.2]).reshape((2, 1))
    container.dist_to_boundary(position)