# -*- coding:utf-8 -*-
# @author :adolf
from functools import reduce
import operator
import math
import numpy as np
from scipy import spatial

coords = [(241, 124), (249, 124), (249, 121), (241, 120)]
center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), coords), [len(coords)] * 2))

coords = sorted(coords, key=lambda coord: (-135 - math.degrees(
    math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)

print(coords)

coords = [(241, 124), (249, 124), (249, 121), (241, 120)]
origin = [241, 120]
refvec = [0, 1]


def clockwiseangle_and_distance(point):
    # Vector between point and the origin: v = p - o
    vector = [point[0] - origin[0], point[1] - origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0] / lenvector, vector[1] / lenvector]
    dotprod = normalized[0] * refvec[0] + normalized[1] * refvec[1]  # x1*x2 + y1*y2
    diffprod = refvec[1] * normalized[0] - refvec[0] * normalized[1]  # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2 * math.pi + angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector


# print(sorted(coords, key=clockwiseangle_and_distance))

coords_ = [[53, 424], [784, 443], [784, 423], [52, 443]]


def _order_points(pts):
    pts = np.array(pts)
    x_sorted = pts[np.argsort(pts[:, 0]), :]

    left_most = x_sorted[:2, :]
    right_most = x_sorted[2:, :]

    left_most = left_most[np.argsort(left_most[:, 1]), :]
    (tl, bl) = left_most

    distance = spatial.distance.cdist(tl[np.newaxis], right_most, 'euclidean')[0]

    (br, tr) = right_most[np.argsort(distance)[::-1], :]

    return np.array([tl, tr, br, bl], dtype='int')


print(_order_points(coords_))
