# -*- coding:utf-8 -*-
# @author :adolf
import os
import json
# from functools import reduce
# import operator
# import math
from scipy import spatial
import numpy as np
from scipy.spatial import distance as dist

data_path = '/datadisk4/SynthText/miao/miaodata/'


def order_points(pts):
    pts = np.array(pts)
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
    D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
    (br, tr) = rightMost[np.argsort(D)[::-1], :]

    # return the coordinates in top-left, top-right,
    # bottom-right, and bottom-left order
    return np.array([tl, tr, br, bl], dtype="float32")


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
    # return [tl, tr, br, bl]


def handle_gt_json_to_txt(data_path):
    data_list = os.listdir(data_path)
    label_list = [label_name for label_name in data_list if 'json' in label_name]

    # label_list = ['20191025161207.json']
    for gt_name in label_list:
        # print(gt_name)
        gt_path = os.path.join(data_path, gt_name)
        try:
            with open(gt_path, 'r') as f:
                json_str = f.read()
                gt_dict = json.loads(json_str)
                gt_list = gt_dict['shapes']
                # gt_label = gt_list['']
                new_gt_name = 'gt_' + gt_name.replace('json', 'txt')
            gt_txt_path = os.path.join(data_path, new_gt_name)
            # print(gt_txt_path)
            with open(gt_txt_path, 'w') as fg:
                for one_gt in gt_list:
                    points = one_gt['points']
                    labels = one_gt['label']

                    # print(points)
                    # print('1111', points)

                    points = order_points(points)
                    points_ = _order_points(points)
                    # print('2222', points)
                    # if points == point:
                    #     print('111', point)
                    fg.write(str(int(points[0][0])))
                    fg.write(',')
                    fg.write(str(int(points[0][1])))
                    fg.write(',')
                    fg.write(str(int(points[1][0])))
                    fg.write(',')
                    fg.write(str(int(points[1][1])))
                    fg.write(',')
                    fg.write(str(int(points[2][0])))
                    fg.write(',')
                    fg.write(str(int(points[2][1])))
                    fg.write(',')
                    fg.write(str(int(points[3][0])))
                    fg.write(',')
                    fg.write(str(int(points[3][1])))
                    fg.write(',')
                    fg.write(str(labels))
                    fg.write('\n')
        except Exception as e:
            print(e)
            print(gt_path)
            print(points)
            print(labels)


def rename_file(file_path):
    da_l = os.listdir(file_path)

    for da_n in da_l:
        oldname = os.path.join(file_path, da_n)

        da_n = da_n.replace('未命名', '')
        newname = file_path + da_n

        os.rename(oldname, newname)
        print(oldname, '======>', newname)


if __name__ == '__main__':
    # rename_file('/datadisk4/SynthText/miao/miaodata/')
    #
    handle_gt_json_to_txt(data_path)
    # 15, 464, 340, 484, 341, 463, 15, 482
