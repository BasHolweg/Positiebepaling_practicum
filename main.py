import matplotlib.pyplot as plt
import numpy as np
import plotter as p
import geometry as g
from trilaterate2d import trilaterate


def noise(array, d=0.0):
    for i in range(len(array)):
        array[i] += d * np.random.random()
    return array


def trilaterate2d_grid(points, a, b, c, a_d, b_d, c_d):
    data = []
    for i in range(len(points)):
        try:
            point = trilaterate(a, b, c, a_d[i], b_d[i], c_d[i], variant=3)
            data.append(point)
        except ValueError:
            print("No point found")
            continue
    return np.array(data)


def create_grid(x_size=10, y_size=10, z_size=None):
    c = []
    for x in range(x_size):
        for y in range(y_size):
            if z_size:
                for z in range(z_size):
                    c.append([x, y, z])
            else:
                c.append([x, y])
    return np.array(c)


def point_array_diff(a1, a2):
    if len(a1) != len(a2):
        raise ValueError("Arrays are not of the same size. Impossible to calculate")
    else:
        diff_array = []
        for i in range(len(a1)):
            diff_array.append(g.distance(a1[i], a2[i]))
        return np.array(diff_array)


def array_to_point_dist(array, point):
    dist_array = []
    for i in range(len(array)):
        dist_array.append(g.distance(array[i], point))
    return np.array(dist_array)


version = 1
printer = True

coordinates = create_grid(60, 40)
b1 = np.array([10, 20])
b2 = np.array([30, 25])
b3 = np.array([40, 20])

x_space = np.linspace(0, 60, 10)
y_space = np.linspace(0, 40, 10)
ex_count = 1
nd = 0.0001


fig, ax = plt.subplots()

ax.scatter(b1[0], b1[1])
ax.scatter(b2[0], b2[1])
ax.scatter(b3[0], b3[1])

# p.plot_points(coordinates)


if version == 1:
    for x in x_space:
        for y in y_space:
            point = np.array([x, y])
            dist_array = array_to_point_dist([b1, b2, b3], point)
            print(dist_array)
            dist_array = noise(dist_array, nd)
            print(dist_array)

            try:
                pre = trilaterate(b1, b2, b3, dist_array[0], dist_array[1], dist_array[2], variant=3)
            except ValueError:
                print("No solution found")
                continue
            if printer:
                ax.scatter(pre[0], pre[1], marker='+', c='grey')
                ax.scatter(x, y, marker='x', c='r')

else:
    for j in range(len(coordinates)):
        point = coordinates[j]
        dist_array = array_to_point_dist([b1, b2, b3], point)

if printer:
    plt.show()
