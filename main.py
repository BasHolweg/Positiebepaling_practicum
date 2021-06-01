import numpy as np
import plotter as p
import geometry as g


def create_grid(x_size=10, y_size=10, z_size=None):
    c = []
    for x in range(x_size + 1):
        for y in range(y_size + 1):
            if z_size:
                for z in range(z_size + 1):
                    c.append([x, y, z])
            else:
                c.append([x, y])
    return np.array(c)


def array_to_point_dist(array, point):
    dist_array = []
    for i in range(len(array)):
        dist_array.append(g.distance(array[i], point))
    return dist_array


coordinates = create_grid(60,40)
b1 = np.array([10,16])
dist_array = array_to_point_dist(coordinates, b1)
print(len(dist_array))
print(len(coordinates))
p.plot_diff(coordinates, dist_array)
