import numpy as np
import matplotlib.pyplot as plt


# p1 = [x,y]


def create_grid(x_size, y_size, z_size=None):
    c = []
    for x in range(x_size):
        for y in range(y_size):
            if z_size:
                for z in range(z_size):
                    c.append([x, y, z])
            else:
                c.append([x, y])
    return np.array(c)


coordinates = create_grid(60, 40)
print(coordinates)
print(coordinates[2399])
print(len(coordinates))
