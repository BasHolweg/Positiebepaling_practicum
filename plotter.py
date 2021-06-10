"""
Plotting toolset developed for PosBep-P1 assignment

Bas Holweg 10-06-2021
"""


import numpy as np
import matplotlib.pyplot as plt
import trilaterate2d as tr2d


def plot_points(points, color='red', size=5):
    """Plots all points in list"""
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


def plot_diff(point, distarray):
    """Plots 3d graph of point coordinates in relation to the deviation"""
    x, y, z = [], [], []
    if len(point) > 2:
        for i in range(len(point)):
            x.append(point[i][0])
            y.append(point[i][1])
            z.append(distarray[i])
        x, y, z = np.array(x), np.array(y), np.array(z)
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        surf = ax.plot_trisurf(x, y, z, cmap='inferno', linewidth=0.1)
    else:
        for i in range(len(point)):
            x.append(point[0])
            y.append(point[1])
            z.append(distarray[i])
        x, y, z = np.array(x), np.array(y), np.array(z)
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        surf = ax.plot_trisurf(x, y, z, cmap='inferno', linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)


def visualise_trilat2d(point, a, b, c, a_distances, b_distances, c_distances):
    """Visualises trilateration method for determening point"""
    inter_points = tr2d.circle_intersect(a, b, a_distances[point], b_distances[point])

    print(f"Intersection points are {inter_points[0]} and {inter_points[1]}")

    draw_circle = plt.Circle(a, a_distances[point], fill=False)
    draw_circle2 = plt.Circle(b, b_distances[point], fill=False)
    draw_circle3 = plt.Circle(c, c_distances[point], fill=False)

    plt.gca().add_artist(draw_circle)
    plt.gca().add_artist(draw_circle2)
    plt.gca().add_artist(draw_circle3)

    plot_points([a, b, c, inter_points[0], inter_points[1]])

