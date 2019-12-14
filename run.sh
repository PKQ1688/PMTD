#!/usr/bin/env bash
CUDA_VISIBLE_DEVICES=0 \
python demo/PMTD_demo.py \
--image_path=/home/shizai/adolf/ocr/miao_ocr_project/data/test_miao/miao_4.jpeg \
--model_path=models/PMTD_ICDAR2017MLT.pth \
--output_type=Image #Image,Points
#--image_path=/home/shizai/adolf/ocr/ocr_project_use/shenzhou_project/data/001.jpg \
