import numpy as np
import geometry as g

def noise(array, nd=0.0):
    for i in range(len(array)):
        array[i] += nd * np.random.uniform(-1, 1)
    return array


def create_grid(x_size=10, y_size=10, z_size=None):
    c = []
    for x in range(x_size+1):
        for y in range(y_size+1):
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


def array_to_point_dist(array, p):
    d_array = []
    for i in range(len(array)):
        d_array.append(g.distance(array[i], p))
    return np.array(d_array)
