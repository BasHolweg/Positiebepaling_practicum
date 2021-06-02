""" 
   Set of functions for 3D trilateration

   Developed for the course PosBep (Positiebepaling) at Mechatronics, 
   The Hague University of Applied Sciences

   No Warranty

   Rufus Fraanje, GNU-GPLv3, 2021/05/08
"""

import numpy as np
from geometry import *


def is_on_sphere(c, r, p):
    """is_on_sphere(c,r,p) returns True when point p is at a distance of radius r of point c, the center of the circle or sphere, else returns False"""
    return np.isclose(distance(c, p), r)


def is_intersecting(c1, c2, r1, r2):
    """is_intersecting(c1,c2,r1,r2) returns True of both spheres or circles with midpoint c1 and c2 and radius r1 and r2 intersect, else returns False."""
    d = distance(c1, c2)
    if np.abs(r1 - r2) <= d and d <= r1 + r2:
        return True
    else:
        return False


def sphere_intersections(c1, c2, c3, r1, r2, r3):
    """sphere_intersections(c1,c2,c3,r1,r2,r3) returns the two intersection points (that can be equal) of three spheres with center c1, c2, c3 and radii r1, r2 r3 respectively."""

    if is_collinear(c1, c2, c3):
        raise ValueError('c1, c2 and c3 should not be collinear, i.e. should not lay on a straight line.')
    if not (is_intersecting(c1, c2, r1, r2) and is_intersecting(c1, c3, r1, r3) and is_intersecting(c2, c3, r2,
                                                                                                    r3)):  # degenerate situation: no intersections
        raise ValueError('There are no intersection points, two or three spheres do not intersect.')

    d21 = c2 - c1  # direction from c1 to c2
    d31 = c3 - c1  # direction from c1 to c3
    v1 = normalized(d21)  # v1 points in direction of c1 to c2
    _, v2, _ = projection_rejection_reflection(v1, d31)  # v2 is orthogonal to v1 and lies in plane of c1,c2,c3
    v2 = normalized(v2)
    v3 = np.cross(v1, v2)  # v3 is perpendicular to plane of c1,c2,c3, and thus perpendicular to v1 and v2

    # note v1,v2,v3 are unit length vectors, v1^T*v1 = v2^T*v2 = v3^T*v3 = 1, and orthogonal, v1^T*v2 = v1^T*v3 = v2^T*v3 = 0
    alpha2 = np.dot(v1,
                    d21)  # c2 = c1 + alpha2 * v1 -> alpha2 = v1^T*(c2-c1); note alpha2 is not 0, because c2-c1 is not zero and not perpendicular to v1
    alpha3 = np.dot(v1, d31)  # c3 = c1 + alpha3 * v1 + beta3 * v2 -> alpha3 = v1^T*(c3-c1),
    beta3 = np.dot(v2,
                   d31)  # -> beta3 = v2^T*(c3-c1), note beta3 is not 0, because c3-c1 is not zero and not perpendicular to v2

    alpha = (r1 ** 2 - r2 ** 2 + alpha2 ** 2) / (2 * alpha2)  # alpha2 cannot be zero, so no check is needed here
    beta = (r1 ** 2 - r3 ** 2 - 2 * alpha3 * alpha + alpha3 ** 2 + beta3 ** 2) / (
                2 * beta3)  # beta3 cannot be zero, so no check is needed here
    gamma = np.sqrt(
        r1 ** 2 - alpha ** 2 - beta ** 2)  # if all three spheres intersect, alpha**2 + beta**2 <= r1**2, so no imaginary solutions

    p1 = c1 + alpha * v1 + beta * v2 + gamma * v3
    p2 = c1 + alpha * v1 + beta * v2 - gamma * v3

    return p1, p2


def trilaterate(c1, c2, c3, c4, r1, r2, r3, r4):
    """trilaterate(c1,c2,c3,c4,r1,r2,r3,r4) returns the intersection point of the 4 intersecting spheres with
       non-coplanar midpoints c1,c2,c3,c4 and radii r1,r2,r3,r4."""

    # first check if c1,c2,c3 and c4 are coplanar
    if is_coplanar(c1, c2, c3, c4):
        raise ValueError('c1, c2, c3 and c4 should not be coplanar, i.e. should not lay in same plane.')

    try:
        sol123 = sphere_intersections(c1, c2, c3, r1, r2, r3)
        sol124 = sphere_intersections(c1, c2, c4, r1, r2, r4)
        sol134 = sphere_intersections(c1, c3, c4, r1, r3, r4)
        sol234 = sphere_intersections(c2, c3, c4, r2, r3, r4)
    except ValueError as e:
        raise e

    indices = nearest_points(sol123, sol124, sol134, sol234)
    return (sol123[indices[0]] + sol124[indices[1]] + sol134[indices[2]] + sol234[indices[3]]) / 4
