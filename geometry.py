""" 
   Set of functions for doing geometry, e.g. in 2D and 3D

   Developed for the course PosBep (Positiebepaling) at Mechatronics, 
   The Hague University of Applied Sciences

   No Warranty

   Rufus Fraanje, GNU-GPLv3, 2021/05/01
"""

import numpy as np


def length(v):
    """length(v) returns the length of vector v."""
    if np.all(np.isclose(v,0)):
        return 0.0
    else:
        return np.linalg.norm(v)

    
def is_zero_length(v):
    """is_zero_length(v) returns True when all elements in vector v are zero."""
    return np.all(np.isclose(v,0))


def is_equal(p1,p2):
    """is_equal(p1,p2) returns True of p1 and p2 are points or vectors with the same coordinates."""
    return np.all(np.isclose(p1,p2))


def distance(p1,p2):
    """distance(p1,p2) returns distance between p1 and p2."""
    if np.all(np.isclose(p1,p2)):
        return 0.0
    else:
        return length(p1-p2)


def projection_rejection_reflection(v,w):
    """projection_rejection_reflection(v,w) returns the projection, rejection and reflection of w on/in v.      
       projection of w on v is the vector w_p = (v^T w / (v^T v) ) v,
           note w_p is along v, it's the part of w that is parallel to v
       rejection  of w on v is the vector w_r = w - w_p, or w = w_p + w_r
           note that w_r is perpendicular to v and in plane spanned by v, w
       reflection of w in v is the vector w_f = w - 2 w_r, 
           so w_f = w_p - w_r, and w_f has same length as w, but mirrored in v.
    """

    vw = np.dot(v,w)
    vv = np.dot(v,v)

    if np.isclose(vv,0):
        raise ValueError('Vector v should not be of zero length.')
    else:
        w_p = (vw/vv)*v  # projection of w on v
        w_r = w - w_p    # rejection of w in v
        w_f = w - 2*w_r  # reflection of w in v
    
        return w_p, w_r, w_f

    
def normalized(v):
    """normalized(v) returns the unit-vector with the same direction as v."""
    if is_zero_length(v):
        raise ValueError('Vector v should not be of zero length.')
    else:
        return v/length(v)

    
def is_collinear(p1,p2,p3):
    """is_collinear(p1,p2,p3) returns True of p1, p2 and p3 lay on a straight line
    (i.e. they are collinear), else returns False."""

    # first check if at least two points are the same, then for sure the points are collinear:
    if is_equal(p1,p2) or is_equal(p1,p3) or is_equal(p2,p3):
        return True
    else: # check if rejection op p3 on line through p1, p2 is zero, then also collinear:
          # this is same as checking if rejection of vector p3-p1 on p2-p1 is zero:
        _,p3_rej_p1_p2,_ = projection_rejection_reflection(p2-p1,p3-p1)
        return is_zero_length(p3_rej_p1_p2)

    
def is_coplanar(p1,p2,p3,p4):
    """is_coplanar(p1,p2,p3,p4) returns True of p1, p2, p3 and p4 are all in one plane, else returns False."""
    # first check if at least three points are collinear:
    if is_collinear(p1,p2,p3) or is_collinear(p1,p2,p4) or is_collinear(p1,p3,p4) or is_collinear(p2,p3,p4):
        return True
    else: # construct a vector v perpendicular to the vectors p2-p1 and p3-p1
        v = np.cross(p2-p1,p3-p1)
        # if projection of p4-p1 on v is zero, than p4-p1 is in plane of p2-p1 and p3-p1, so coplanar
        p41_proj_v,_,_ = projection_rejection_reflection(v,p4-p1)
        return is_zero_length(p41_proj_v)


def nearest_points(*pairs):
    """nearest_points(*pairs) returns a list with indices 0 or 1 indicating which of the
    two points in all pairs are closest to each other. Used in trilateration problems to
    find the corresponding solutions in multiple pairs."""
    num_points = len(pairs)
    indices = np.zeros(num_points,dtype=np.int8)

    # first check first two pairs
    dist = np.argsort([distance(pairs[0][0],pairs[1][0]),
                       distance(pairs[0][0],pairs[1][1]),
                       distance(pairs[0][1],pairs[1][0]),
                       distance(pairs[0][1],pairs[1][1])])
    if dist[0] == 0:
        indices[0], indices[1] = 0, 0
    elif dist[0] == 1:
        indices[0], indices[1] = 0, 1
    elif dist[0] == 2:
        indices[0], indices[1] = 1, 0
    else:
        indices[0], indices[1] = 1, 1

    # compare the remaining pairs using the selected point in the first pair as reference
    reference = pairs[0][indices[0]]
    for n in range(num_points-2):
        indices[n+2] = 0 if (distance(reference,pairs[n+2][0]) <= distance(reference,pairs[n+2][1])) else 1

    return indices

