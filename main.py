"""
Assignment PosBep-P1



Bas Holweg 10-06-2021
"""


import matplotlib.pyplot as plt
import numpy as np
from plotter import plot_diff
from geometry import distance
from tools import create_grid, noise, array_to_point_dist
from trilaterate2d import trilaterate

version = 2
show_plots = True           # Used for debugging
variable_deviation = False  # If True it plots the noise relation else it plots a 3d graph of the set deviation

ex_count = 5  # Number of experements done per point

if variable_deviation:
    nd_list = np.linspace(0.01, 0.1, 10)
else:
    nd_list = [0.01]

# Used for version 1
x_space = np.linspace(0, 60, 60)
y_space = np.linspace(0, 40, 40)
b1 = np.array([15, 15])
b2 = np.array([30, 35])
b3 = np.array([45, 15])

# Used for version 2
x_size, y_size = 60, 40
coordinates = create_grid(x_size, y_size)
b12 = np.array([int(x_size/4), int(y_size/4)])
b22 = np.array([int(x_size/2), int(2*y_size/3)])
b32 = np.array([int(2*x_size/3), int(y_size/4)])

fig, ax = plt.subplots()
fig2, ax2 = plt.subplots()

if version == 1:
    # Plots the beacons
    ax.scatter(b1[0], b1[1])
    ax.scatter(b2[0], b2[1])
    ax.scatter(b3[0], b3[1])

    total_diff_sum = 0
    total_diff = []
    for nd in nd_list:
        diff = []
        point_list = []
        for x in x_space:
            for y in y_space:
                point = np.array([x, y])
                point_list.append(point)
                dist_array = array_to_point_dist([b1, b2, b3], point)
                if len(nd_list) == 1: ax.scatter(x, y, marker='+', c='r')  # Only plot if there is one deviation value to prevent multiple plots showing and slowing down the program
                diff_sum = 0
                count = 0
                for q in range(ex_count):
                    dist_array = noise(dist_array, nd)
                    try:
                        pre = trilaterate(b1, b2, b3, dist_array[0], dist_array[1], dist_array[2], variant=3)
                        diff_sum += distance(pre, point)
                        count += 1
                        if len(nd_list) == 1: ax.scatter(pre[0], pre[1], marker='x', c='grey')
                    except ValueError:
                        count -= 1
                        continue
                if count != 0:  # If there are points found add the average deviation to list
                    diff.append(diff_sum/count)
                else:  # If no points are found assume standard deviation
                    diff.append(nd)
        if len(nd_list) == 1: plot_diff(point_list, diff)
        total_diff.append(sum(diff) / len(diff))
    if len(nd_list) > 1:
        ax2.plot(nd_list, total_diff)
        ax2.set_ylabel("Average error distance [m]")
        ax2.set_xlabel("Standard deviation [m]")

else:
    ax.scatter(b12[0], b12[1])
    ax.scatter(b22[0], b22[1])
    ax.scatter(b32[0], b32[1])
    total_diff_sum = 0
    total_diff = []
    for nd in nd_list:
        diff = []
        for j in range(len(coordinates)):
            point = coordinates[j]
            dist_array = array_to_point_dist([b12, b22, b32], point)
            if len(nd_list) == 1: ax.scatter(point[0], point[1], marker='+', c='r')
            diff_sum = 0
            count = 0
            for q in range(ex_count):
                try:
                    dist_array = noise(dist_array, nd)
                    pre = trilaterate(b12, b22, b32, dist_array[0], dist_array[1], dist_array[2], variant=3)
                    diff_sum += distance(pre, point)
                    count += 1
                    if len(nd_list) == 1: ax.scatter(pre[0], pre[1], marker='x', c='grey')
                except ValueError:
                    count -= 1
                    # print(f"No solution found for {point}")
                    continue
            if count != 0:
                diff.append(diff_sum / count)
            else:
                diff.append(nd)
        if len(nd_list) == 1: plot_diff(coordinates, diff)
        total_diff.append(sum(diff) / len(diff))
    if len(nd_list) > 1:
        ax2.plot(nd_list, total_diff)
        ax2.set_ylabel("Average error distance [m]")
        ax2.set_xlabel("Standard deviation []")

if show_plots:
    plt.show()
