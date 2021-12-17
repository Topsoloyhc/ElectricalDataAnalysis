import os

import numpy as np
import pandas as pd
import utils
import json
import sys

from matplotlib import pyplot as plt
from output import Out2txt

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 解决plt不能显示中文的解决方法
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def elect_identify_1(d_file, j_file, out_type):
    '''
    Parameters
    ----------
    d_file: 输入文件地址
    j_file： 存储电器特征的json文件
    out_type： 输出的类型，记录在输出文件名中
    '''
    # sys.stdout = Out2txt(sys.stdout, out_type)  # 将输出记录到txt中
    # sys.stderr = Out2txt(sys.stderr, out_type)  # 将错误信息记录到txt中

    with open(j_file) as file_obj:
        power_feature = json.load(file_obj)

    count_power = utils.power_data_process(d_file)
    # print(len(count_power))

    status = []
    for i in range(1, int(len(count_power) / 500) + 1):
        record = []
        for j in range(27):
            record.append(
                utils.eucldist_vectorized(count_power[(i - 1) * 500:i * 500], power_feature[j]["power_feature"]))
        index = utils.findSmallest(record)
        now_data = power_feature[index]
        status.append([0.5 * i, now_data["label"], now_data["name"]])
        if now_data["label"] == 0:
            print("label " + str(now_data["label"]) + ", 当前第" + str(0.5 * i) + "秒，无电器运行")
        else:
            if now_data["type"] == 1:
                print(
                    "label " + str(now_data["label"]) + ", 当前第" + str(0.5 * i) + "秒，处于" + now_data["name"] + ", 为稳定状态")
            else:
                print(
                    "label " + str(now_data["label"]) + ", 当前第" + str(0.5 * i) + "秒，处于" + now_data["name"] + ", 为切换状态")
    print(status)
    #
    s_len = len(status)
    plt.figure(figsize=(15, 8), dpi=100)
    plt.xticks([i for i in range(s_len)], [str(status[j][0]) + "秒" for j in range(s_len)], rotation=30)
    # plt.yticks([i for i in range(27)], ['无电器运行', '吹风机0-1档', '吹风机1-2档', '吹风机2-1档', '吹风机1-0档', '吹风机0-2档',
    #                                     '吹风机2-0档', '吹风机  1档', '吹风机  2档', '小电锅0-1档', '小电锅1-0档', '小电锅0-2档',
    #                                     '小电锅2-0档', '小电锅  1档', '小电锅  2档', '吸尘器0-1档', '吸尘器1-0档','吸尘器  1档',
    #                                     '热风机0-1档', '热风机1-0档', '热风机  1档', '电熨斗0-1档', '电熨斗1-0档', '电熨斗  1档',
    #                                     '鼓风机0-1档', '鼓风机1-0档', '鼓风机  1档'])

    plt.plot([status[j][1] for j in range(s_len)])
    plt.yticks([])
    for spine in ["left", "top", "right"]:
        plt.gca().spines[spine].set_visible(False)

    plt.scatter([i for i in range(s_len)], [status[j][1] for j in range(s_len)])

    for i in range(s_len):
        plt.annotate(status[i][2], xy=(i, status[i][1]), xytext=(i + 0.1, status[i][1] + 0.1),
                     rotation=45)  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
    plt.show()


def elect_identify_2(d_file, j_file, out_type):
    '''
    Parameters
    ----------
    j_file
    d_file:输入文件地址
    j_file：存储电器特征的json文件
    out_type：输出的类型，记录在输出文件名中
    '''
    # sys.stdout = Out2txt(sys.stdout, out_type)  # 将输出记录到txt中
    # sys.stderr = Out2txt(sys.stderr, out_type)  # 将错误信息记录到txt中

    with open(j_file) as file_obj:
        power_feature = json.load(file_obj)

    data = pd.read_csv(d_file, encoding="gb18030")

    voltage_data = data["CH1(mV)"]
    current_data = data["CH4(mV)"]


if __name__ == "__main__":
    csv_file = "../data/小电锅-19.75-2.csv"
    json_file = "../power_feature.json"

    with open(json_file) as file_obj:
        power_feature = json.load(file_obj)

    # elect_identify_1(csv_file, json_file, "elect_identify_1")

    data = pd.read_csv(csv_file, encoding="gb18030")
    # utils.stft_specgram(data["CH4(mV)"], '小电锅')
    utils.stft_specgram(power_feature[24]["power_feature"], '鼓风机0-1档')
    # print(data)

    # idxs = np.random.randint(10, size=(4 * 4))
    # print(idxs)

    # read_data()
    # identify()
