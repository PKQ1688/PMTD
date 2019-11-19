# -*- coding:utf-8 -*-
# @author :adolf
import os

data_test = '/home/shizai/datadisk4/SynthText/miaodata'

data_list = os.listdir(data_test)

data_list = [data_name for data_name in data_list if 'png' in data_name]

print(data_list)
