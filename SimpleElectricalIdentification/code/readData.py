import os

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import utils

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# 解决plt不能显示中文的解决方法
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


if __name__ == "__main__":
    csv_file = "../data/电熨斗-14.75-1.csv"
    # data = pd.read_csv(csv_file, encoding="gb18030")
    #
    # instance_power = [a * b for a, b in zip(data['CH1(mV)'], data['CH4(mV)'])]  # 瞬时功率
    # add_zero = [0.0] * 10
    # instance_power = add_zero + instance_power + add_zero
    # # instance_power = np.array(instance_power)
    # count_power = []  # 有功功率
    # for i in range(9, len(instance_power) - 10):
    #     # count_power.append(-(sum(instance_power[i - 10:i + 10]) / 20))
    #     count_power.append(sum(instance_power[i - 10:i + 10]) / 20)

    count_power = utils.power_data_process(csv_file)
    print(len(count_power))
    # print(count_power[1980:2010])

    plt.subplot(211)
    plt.plot(count_power, label="Count_Power")
    # plt.show()
    #
    start = 6000
    end = 6500
    plt.subplot(212)
    plt.plot(count_power[start:end], label="Count_Power")
    plt.show()
    #
    print("min: " + str(min(count_power[start:end])), ",max: " + str(max(count_power[start:end])), ",ΔP: " + str(max(count_power[start:end]) - min(count_power[start:end])))
    # print("Δt = 100")
    #
    cnt = 0
    for i in range(20, len(count_power) - 10, 20):
        if(max(count_power[i-10:i+10]) - min(count_power[i-10:i+10])) > 20000:
            cnt += 1
            print(i, " ", count_power[i])

    #
    # for i in range(0, len(count_power)-1):
    #     if(abs(count_power[i+1] - count_power[i])) > 20000:
    #         cnt += 1
    #         print(i, " ", count_power[i])
    print(cnt)