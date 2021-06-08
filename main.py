import numpy as np
import plotter as p
import geometry as g
import trilaterate2d as tr2d


def trilaterate2d_grid(points, a, b, c, a_d, b_d, c_d):
    data = []
    for i in range(len(points)):
        if not (points[i] == a).all() or (points[i] == b).all() or (points[i] == c).all():
            data.append(tr2d.trilaterate(a,b,c,a_d[i], b_d[i], c_d[i], variant=1))
        else:
            pass
    return data


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


coordinates = create_grid(60, 40)
b1 = np.array([0, 0])
b2 = np.array([30, 40])
b3 = np.array([60, 0])
b1_distances = array_to_point_dist(coordinates, b1)
b2_distances = array_to_point_dist(coordinates, b2)
b3_distances = array_to_point_dist(coordinates, b3)

tri_points = trilaterate2d_grid(coordinates,b1, b2, b3, b1_distances, b2_distances, b3_distances)

print(tri_points)
