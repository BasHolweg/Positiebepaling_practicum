""" 
   Set of functions for 2D trilateration

   Two variants: based on circle intersection and based on least squares.
   Developed for the course PosBep (Positiebepaling) at Mechatronics, 
   The Hague University of Applied Sciences

   No Warranty

   Rufus Fraanje, GNU-GPLv3, 2021/05/01
"""

import numpy as np
from geometry import *


def is_on_circle(c, r, p):
    """returns True if point p is on the circle with center c and radius r, else returns False"""
    return np.isclose(distance(c, p), r)


def perpendicular(p):
    """perpendicular(p) returns the vector that is 90^o rotation of p, and thus perpendicular to p"""
    return np.array([-p[1], p[0]])


def circle_intersect(c1, c2, r1, r2):
    """circle_intersect(c1,c2,r1,r2) returns the intersection points of two circles
       one with center c1 and radius r1 and the
       other with center c2 and radius r2."""

    d = distance(c1, c2)
    if np.isclose(d, 0) and np.isclose(r1, r2):  # degenerate situation: circles overlap
        raise ValueError('Both circles are equal.')
    if d > r1 + r2 or d < np.abs(r1 - r2):  # degenerate situation: no intersections
        raise ValueError('There are no intersection points.')

    # in following situation with one solution (beta=0) will return two equal solutions
    alpha = ((r1 / d) ** 2 - (r2 / d) ** 2 + 1) / 2
    beta = np.sqrt((r1 / d) ** 2 - alpha ** 2)
    # if np.isclose(beta,0):
    #    print('Only one intersection point, the two points returned are equal.')
    v1 = c2 - c1
    v2 = perpendicular(v1)
    p1 = c1 + alpha * v1 + beta * v2
    p2 = c1 + alpha * v1 - beta * v2

    return p1, p2


def trilaterate(c1, c2, c3, r1, r2, r3, variant=1):
    """trilaterate(c1,c2,c3,r1,r2,r3) returns the point (if it exists) 
       that is at distance r1 to c1, r2 to c2 and r3 to c3.
       The circle centers should not be on a straight line, 
       i.e. the circle centers should form a real triangle.
       variant=1: computes intersections of circle 1 and 2 and checks which lays on circle 3
              =2: tries other combinations of circles and returns the solution closest to the other circle
              =3: computes all pairs of solutions, selects the 3 closest variants in the pairs and returns
                  their average (computationally most complex but expected to be the most accurate solution).
    """
    if is_equal(c1, c2) or is_equal(c1, c3) or is_equal(c2, c3):
        raise ValueError('All beacons should be at different locations, at least two have same location.')

    # check whether c1,c2,c3 are on a straight line
    if is_collinear(c1, c2, c3):
        raise ValueError('c1, c2 and c3 are collinear, but should form a real triangle.')

    if variant == 1:
        # Variant 1:
        c_other, r_other = c3, r3
        p = circle_intersect(c1, c2, r1, r2)

        if is_on_circle(c_other, r_other, p[0]):
            return p[0]
        elif is_on_circle(c_other, r_other, p[1]):
            return p[1]
        else:
            raise ValueError('No solution found.')
    elif variant == 2:
        # Variant 2:
        c_other, r_other = c3, r3
        p = circle_intersect(c1, c2, r1, r2)
        if p is None:
            c_other, r_other = c2, r2
            p = circle_intersect(c1, c3, r1, r3)
            if p is None:
                c_other, r_other = c1, r1
                p = circle_intersect(c2, c3, r2, r3)
                if p is None:
                    raise ValueError('No solution found.')

        if np.abs(distance(p[0], c_other) - r_other) < np.abs(distance(p[1], c_other) - r_other):
            return p[0]
        else:
            return p[1]

    else:
        # Variant 3:
        try:
            sol12 = circle_intersect(c1, c2, r1, r2)
            sol13 = circle_intersect(c1, c3, r1, r3)
            sol23 = circle_intersect(c2, c3, r2, r3)
        except ValueError as e:
            raise e

        indices = nearest_points(sol12, sol13, sol23)
        return (sol12[indices[0]] + sol13[indices[1]] + sol23[indices[2]]) / 3


def trilaterate_lstsq(c, r):
    """Solves a least squares problem to estimate the point that is at distance r[i] of 
       circle with center at (c[0,i], c[1,i]).

       The problem is made linear by introducing a slack variable q = x^2+y^2 so we can write:
       (x-x_i)^2 + (y-y_i^2) = q^2 -2x_i y - 2y_i x + x_i^2+y_i^2 = [1 -2x_i -2y_i] [ q ] + x_i^2+y_i^2
                                                                                    [ y ]
                                                                                    [ x ]
       this should be as close to r_i^2 as possible for i ranging over the number of beacons.
       NB: Note, that the A matrix which rows are [1 -2x_i -2y_i]  should be full rank and well conditioned!
       Note, there are other (and better) approaches, e.g. taking q = x^2+y^2 as an additional constraint.
    """
    nb = c.shape[1]
    A = np.hstack((np.ones((nb, 1)), -2 * c.T))
    # print(A)
    b = np.zeros((nb, 1))
    for i in range(nb):
        b[i] = r[i] ** 2 - c[0, i] ** 2 - c[1, i] ** 2  # r_i^2 - x_i^2 - y_i^2
    qyx, res, rank, sv = np.linalg.lstsq(A, b, rcond=1e-10)
    # print(f'res = {res}, rank = {rank}')
    return np.array([qyx[2], qyx[1]])
