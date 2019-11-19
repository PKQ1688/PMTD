# -*- coding:utf-8 -*-
# @author :adolf
import os

data_path = '/home/shizai/datadisk4/SynthText/miaodata'

data_list = os.listdir(data_path)

for data_name in data_list:
    oldname = data_path + os.sep + data_name

    new_data_name = data_name.replace('QQ截图', '')

    newname = data_path + os.sep + new_data_name

    os.rename(oldname, newname)

    print(oldname, '======>', newname)
