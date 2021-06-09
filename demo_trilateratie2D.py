"""
   Demo of 2D trilateration.

   Demo for the course PosBep (Positiebepaling) at Mechatronics,
   The Hague University of Applied Sciences

   No Warranty

   Rufus Fraanje, GNU-GPLv3, 2021/05/01
"""

import numpy as np
from matplotlib import pyplot as plt

from geometry import *
from trilaterate2d import circle_intersect, trilaterate, trilaterate_lstsq

# beacon positions
b1 = np.array([0,0])
b2 = np.array([-2,-1])
b3 = np.array([2,0])


x_list = np.linspace(-15,15,10)  # locations to be estimated along x-axis
y_list = x_list   # idem along y-axis
Nexp = 5        # number of experiments per position
std_noise = 0.02   # standard deviation of noise on distance measurements, e.g. 0.02
variant = 3       # determines variant in trialateration algorithm
                  # when std_noise > 0, choose variant = 2 or 3

# # initial test:
# p = np.array([1,1])
# r = np.array([distance(p,b) for b in [b1,b2,b3]])
# print('circle intersection:',circle_intersect(b1,b2,r[0],r[1]))


fig,ax = plt.subplots()
# plotting of beacons, zorder is to show them in front of the estimations
ax.plot(b1[0],b1[1],'bo',ms=14,zorder=1)
ax.plot(b2[0],b2[1],'bo',ms=14,zorder=1)
ax.plot(b3[0],b3[1],'bo',ms=14,zorder=1)


for x in x_list:
    for y in y_list:
        p = np.array([x,y])
        r = np.array([distance(p,b) for b in (b1,b2,b3)])
        # plotting of true position, zorder is to show them in front of the estimations
        ax.plot(p[0],p[1],'r+',ms=14,zorder=1)

        for n in range(Nexp):
            v = std_noise*np.random.randn(*r.shape)  # measurement noise
            dm = r + v  # measured distances, poluted by noise
            try:
                pem = trilaterate(b1,b2,b3,dm[0],dm[1],dm[2],variant=variant)

                # zorder needed in plotting to show estimations behind true positions,
                # therefore it has lower value than of true locations and beacons
                ax.plot(pem[0],pem[1],'x',color='grey',ms=10,zorder=0)
            except:
                print(f'No solution: x = {x}, y = {y}, n = {n}')
                continue

# plt.savefig('plot.pdf')
plt.show()
