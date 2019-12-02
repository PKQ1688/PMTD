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

coords_ = [[15, 464], [340, 484], [341, 463], [15, 482]]


def _order_points(pts):
    pts = np.array(pts, dtype='int')
    x_sorted = pts[np.argsort(pts[:, 0]), :]

    left_most = x_sorted[:2, :]
    right_most = x_sorted[2:, :]

    left_most = left_most[np.argsort(left_most[:, 1]), :]
    (tl, bl) = left_most

    distance = spatial.distance.cdist(tl[np.newaxis], right_most, 'euclidean')[0]

    (br, tr) = right_most[np.argsort(distance)[::-1], :]

    return np.array([tl, tr, br, bl], dtype='int')


# print(_order_points(coords_))
# h_coords = _order_points(coords_)
#
# print(h_coords[0][0])
# print(h_coords[0][1])
# print(h_coords[1][0])
# print(h_coords[1][1])
# print(h_coords[2][0])
# print(h_coords[2][1])
# print(h_coords[3][0])
# print(h_coords[3][1])

from scipy.spatial import distance as dist
import numpy as np
import cv2


def order_points(pts):
    pts = np.array(pts, dtype='int')
    # sort the points based on their x-coordinates
    xSorted = pts[np.argsort(pts[:, 0]), :]

    # grab the left-most and right-most points from the sorted
    # x-roodinate points
    leftMost = xSorted[:2, :]
    rightMost = xSorted[2:, :]

    # now, sort the left-most coordinates according to their
    # y-coordinates so we can grab the top-left and bottom-left
    # points, respectively
    leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
    (tl, bl) = leftMost

    # now that we have the top-left coordinate, use it as an
    # anchor to calculate the Euclidean distance between the
    # top-left and right-most points; by the Pythagorean
    # theorem, the point with the largest distance will be
    # our bottom-right point
    rightMost = rightMost[np.argsort(rightMost[:, 1]), :]
    print('1111', rightMost)
    (tr, br) = rightMost
    # D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
    # (br, tr) = rightMost[np.argsort(D)[::-1], :]

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="int")


coords_1 = [[8, 540], [89, 559], [90, 541], [9, 559]]

print(order_points(coords_1))
