import os
import sys

import yaml
import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd

import pprint
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy.signal import stft


def load_yaml(path):
    """
    Load YAML file
    """
    _yaml = yaml.safe_load(open(path, "r"))
    return _yaml if _yaml else {}


def load_dat(path, nrows=None):
    # load dat 2 csv, 对UKDAL数据读取
    # 或者用read_table对数据进行读取,是一样的
    file_name = path + '.dat'
    single_csv = pd.read_csv(file_name,
                             sep=' ',
                             # header=0,
                             # names=['time', 'appliance'],
                             # dtype={'time': str, "appliance": int},
                             # parse_dates=['time'],
                             # date_parser=pd.to_datetime,
                             nrows=nrows,
                             # usecols=[0, 1],
                             engine='python'
                             )
    return single_csv


def get_rms(records):
    """
    均方根值 反映的是有效值而不是平均值
    """
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))


def power_data_process(path):
    """
    计算有功功率
    """
    data = pd.read_csv(path, encoding="gb18030")

    instance_power = [a * b for a, b in zip(data['CH1(mV)'], data['CH4(mV)'])]  # 瞬时功率
    add_zero = [0.0] * 10
    instance_power = add_zero + instance_power + add_zero
    # instance_power = np.array(instance_power)
    count_power = []
    for i in range(9, len(instance_power) - 10):
        count_power.append(sum(instance_power[i - 10:i + 10]) / 20)
    return count_power


def power_data_process_rms(data, frequency):
    """
    对瞬时功率数据进行每一个采样周期（frequency个数据点）求rms值
    """
    instance_power = [a * b for a, b in zip(data['CH1(mV)'], data['CH4(mV)'])]  # 瞬时功率
    # print(len(instance_power))
    count_power = []  # rms值
    for i in range(0, len(instance_power), frequency):
        count_power.append(get_rms(instance_power[i:i + frequency]))
    return count_power


def eucldist_vectorized(coords1, coords2):
    """ Calculates the euclidean distance between 2 lists of coordinates. """
    coords1 = np.array(coords1)
    coords2 = np.array(coords2)
    return np.sqrt(np.sum((coords1 - coords2) ** 2))


def findSmallest(arr):
    smallest = arr[0]  # 存储最小的值
    smallest_index = 0  # 存储最小元素的索引
    for i in range(1, len(arr)):
        if arr[i] < smallest:
            smallest = arr[i]
            smallest_index = i
    return smallest_index


def stft_specgram(data, picname=None):  # picname是给图像的名字，为了保存图像
    # 短时傅里叶变换频谱图
    f, t, zxx = stft(data, fs=1/1000, nperseg=20)
    plt.subplot(211)
    plt.pcolormesh(t, f, np.abs(zxx))
    plt.colorbar()
    plt.title(picname + ' STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.subplot(212)
    plt.plot(data)
    plt.tight_layout()
    # if picname is not None:
    #     plt.savefig('..\\picture\\' + str(picname) + '.jpg')  # 保存图像
    plt.show()
    plt.clf()  # 清除画布
