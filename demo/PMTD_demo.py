import argparse
import os

import cv2
import sys

sys.path.append('../')
from demo.PMTD_predictor import PMTDDemo
from demo.inference import PlaneClustering
from maskrcnn_benchmark.config import cfg
from maskrcnn_benchmark.modeling.roi_heads.mask_head.inference import Masker

import numpy as np
from scipy import spatial


def build_parser():
    parser = argparse.ArgumentParser(description="PMTD Single Image Inference")
    parser.add_argument(
        "--image_path",
        default="datasets/icdar2017mlt/ch8_test_images/img_1.jpg",
        metavar="FILE",
        help="path to input image"
    )
    parser.add_argument(
        "--device",
        default="cuda",
        choices=["cuda", "cpu"],
        help="test device"
    )
    parser.add_argument(
        "--longer_size",
        type=int,
        default=1600,
        help="test scale for image"
    )
    parser.add_argument(
        "--method",
        default="PlaneClustering",
        choices=["PlaneClustering", "HardThreshold"],
        help="postprocess method for text mask"
    )
    parser.add_argument(
        "--output_type",
        default="Image",
        choices=["Image", "Points"],
        help="output type for predicted results"
    )
    parser.add_argument(
        "--model_path",
        default="models/PMTD_ICDAR2017MLT.pth",
        metavar="FILE",
        help="path to pretrained model"
    )
    return parser


def create_pmtd_demo(args):
    cfg.merge_from_file("configs/e2e_PMTD_R_50_FPN_1x_ICDAR2017MLT_test.yaml")
    cfg.merge_from_list([
        'MODEL.DEVICE', args.device,
        'MODEL.WEIGHT', args.model_path,
        'INPUT.MAX_SIZE_TEST', args.longer_size,
    ])

    if args.method == 'PlaneClustering':
        masker = PlaneClustering()
    else:
        masker = Masker(threshold=0.01, padding=1)

    pmtd_demo = PMTDDemo(
        cfg,
        masker=masker,
        confidence_threshold=0.5,
        show_mask_heatmaps=True,
    )

    return pmtd_demo


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


def main():
    parser = build_parser()
    args = parser.parse_args()
    pmtd_demo = create_pmtd_demo(args)
    assert os.path.exists(args.image_path), "No such image"
    image = cv2.imread(args.image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if args.output_type == "Image":
        predictions = pmtd_demo.run_on_opencv_image(image)
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.resizeWindow('image', 800, 800)
        # cv2.imshow('image', predictions[:, :, ::-1])
        # cv2.waitKey(0)

        ori_image = image.copy()
        predictions = pmtd_demo.compute_prediction(image)
        top_predictions = pmtd_demo.select_top_predictions(predictions)
        bboxes = top_predictions.bbox
        print('22222', bboxes)
        for box in bboxes:
            cv2.rectangle(image, (int(box[0].item()), int(box[1].item())),
                          (int(box[2].item()), int(box[3].item())), (255, 0, 0), 2)
        print('111', predictions)

        cv2.imwrite('./data_test/1.png', image)
    else:
        predictions = pmtd_demo.compute_prediction(image)
        top_predictions = pmtd_demo.select_top_predictions(predictions)

        bboxes = top_predictions.bbox
        masks = top_predictions.extra_fields['mask']
        scores = top_predictions.extra_fields['scores']

        img_name = os.path.basename(args.image_path)
        file_name = 'res_' + img_name.replace('png', 'txt')
        predict_file = os.path.join('/home/shizai/adolf/ai+rpa/ocr/ocr_use/PMTD/res_miao', file_name)

        with open(predict_file, 'w') as f:
            for bbox, mask, score in zip(bboxes, masks, scores):
                print(bbox, mask[0], score)

                masks = mask[0]
                masks = _order_points(masks)
                print(masks)
                f.write(str(int(masks[0][0].item())))
                f.write(',')
                f.write(str(int(masks[0][1].item())))
                f.write(',')
                f.write(str(int(masks[1][0].item())))
                f.write(',')
                f.write(str(int(masks[1][1].item())))
                f.write(',')
                f.write(str(int(masks[2][0].item())))
                f.write(',')
                f.write(str(int(masks[2][1].item())))
                f.write(',')
                f.write(str(int(masks[3][0].item())))
                f.write(',')
                f.write(str(int(masks[3][1].item())))
                # f.write(',')
                f.write('\n')


if __name__ == '__main__':
    main()
