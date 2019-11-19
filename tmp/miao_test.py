# -*- coding:utf-8 -*-
# @author :adolf
import os

data_test = '/datadisk4/SynthText/miao/img'

data_list = os.listdir(data_test)

data_list = [data_name for data_name in data_list if 'png' in data_name]

# print(data_list)

command_line_1 = 'python demo/PMTD_demo.py --image_path='
command_line_2 = ' --model_path=models/PMTD_ICDAR2017MLT.pth --output_type=Points'
for img_n in data_list:
    # os.system('ls')
    data_path = os.path.join(data_test, img_n)
    print(data_path)
    command_line = command_line_1 + data_path + command_line_2
    print(command_line)
    os.system(command_line)

