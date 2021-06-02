import numpy as np
import matplotlib.pyplot as plt


def plot_points(points, color='red', size=5):
    if np.ndim(points) > 1:
        if len(points[0]) == 3:
            ax = plt.axes(projection='3d')
            for i in range(len(points)):
                ax.scatter(points[i][0], points[i][1], points[i][2], c=color, s=size)
        else:
            for i in range(len(points)):
                plt.scatter(points[i][0], points[i][1], c=color, s=size)
    else:
        if len(points) == 3:
            ax = plt.axes(projection='3d')
            ax.scatter(points[0], points[1], points[2], c=color, s=size)
        else:
            plt.scatter(points[0], points[1], c=color, s=size)
    plt.show()


def plot_diff(point, distarray):
    x, y, z = [], [], []
    for i in range(len(point)):
        x.append(point[i][0])
        y.append(point[i][1])
        z.append(distarray[i])
    x, y, z = np.array(x), np.array(y), np.array(z)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    surf = ax.plot_trisurf(x, y, z, cmap='inferno', linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()
