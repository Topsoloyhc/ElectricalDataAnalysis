import json
import os
import numpy as np

import pandas as pd
from matplotlib import pyplot as plt
import numpy.fft as fft
import utils
from scipy import signal

# 解决plt不能显示中文的解决方法
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


def showData_1(data):
    plt.figure(figsize=(15, 10), dpi=80)
    plt.figure(1)

    plt.subplot(321)
    plt.plot(data['CH4(mV)'])
    plt.title("original_current", fontsize=14)
    plt.grid(axis='y')

    plt.subplot(322)
    plt.plot(data['CH4(mV)'][::10])
    plt.title("0-,10", fontsize=14)
    plt.grid(axis='y')

    plt.subplot(323)
    plt.plot(data['CH4(mV)'][10000:20000])
    plt.title("10000-20000", fontsize=14)
    plt.grid(axis='y')

    plt.subplot(324)
    plt.plot(data['CH4(mV)'][10000:20000:10])
    plt.title("10000-20000,10", fontsize=14)
    plt.grid(axis='y')

    plt.subplot(325)
    plt.plot(data['CH4(mV)'][1960:2460])
    plt.title("1960-2460", fontsize=14)
    plt.grid(axis='y')

    plt.subplot(326)
    plt.plot([n for n in data['CH4(mV)'][1960:2460:10]])
    plt.title("1960-2460,10", fontsize=14)
    plt.grid(axis='y')

    plt.show()


def showData_2(data):
    plt.figure(figsize=(15, 10), dpi=80)
    plt.figure(1)

    plt.subplot(311)
    plt.plot(data['CH1(mV)'])
    plt.title("Voltage", fontsize=14)
    plt.grid(axis='y')

    plt.subplot(312)
    plt.plot(data['CH4(mV)'])
    plt.title("Current", fontsize=14)
    plt.grid(axis='y')

    plt.subplot(313)
    plt.plot([a * b for a, b in zip(data['CH1(mV)'], data['CH4(mV)'])])
    plt.title("Power", fontsize=14)
    plt.grid(axis='y')

    plt.show()


def showData_3(data):
    '''
        展示电流数据的离散傅里叶变换的情况
    '''
    # data = [a * b for a, b in zip(data['CH1(mV)'], data['CH4(mV)'])] # 功率
    data = data['CH4(mV)']  # 电流
    complex_array = fft.fft(data)  # 计算一维离散傅里叶变换
    # complex_array = fft.rfft(data)  # 计算实际输入的一维离散傅里叶变换
    print("一维离散傅里叶变换结果长度：" + str(len(complex_array)))

    plt.subplot(311)
    plt.grid(linestyle=':')
    plt.plot(data[0:10000], label='current')
    plt.xlabel("时间（毫秒）")
    plt.ylabel("信号值")
    plt.title("电熨斗-0:10000-电流信号图")
    plt.legend()

    plt.subplot(312)
    data_ifft = fft.ifft(complex_array)  # 计算一维逆离散傅立叶逆变换
    # data_irfft = fft.irfft(complex_array)  # 计算rfft的逆数
    print("一维逆离散傅立叶逆变换后结果长度:" + str(len(data_ifft)))

    plt.plot(data_ifft[0:10000], label='data_ifft', color='orangered')
    plt.xlabel("时间（毫秒）")
    plt.ylabel("data_ifft变换值")
    plt.title("ifft变换图")
    plt.grid(linestyle=':')
    plt.legend()

    # 得到分解波的频率序列
    freqs = fft.fftfreq(10000, 1 / 1000)
    # freqs = fft.rfftfreq(10000, 1/1000)  # 返回离散傅里叶变换采样频率（用于 rfft、irfft）
    # 复数的模为信号的振幅（能量大小）
    pows = np.abs(complex_array)

    plt.subplot(313)
    plt.title('FFT变换,频谱图')
    plt.xlabel('Frequency 频率')
    plt.ylabel('Power 功率')
    # plt.tick_params(labelsize=10)
    plt.grid(linestyle=':')
    # plt.plot([i for i in range(4999)], pows[:10000][freqs > 0], c='orangered', label='Frequency')
    plt.plot(freqs[freqs > 0], pows[:10000][freqs > 0], c='orangered', label='Frequency')
    plt.legend()
    plt.tight_layout()
    plt.show()


def showData_4(data):
    # 尝试以20个数据(一个周期)为一段计算rms值，然后画出数据的曲线查看
    csv_path_1 = "test_data_电器初步检测/吹风机-17.75-2.csv"
    test_data = pd.read_csv(csv_path_1, encoding='gb18030')
    # test_data = pd.read_csv(csv_path_1, names=["Time", "CH1", "CH2", "CH3", "CH4", "CH5", "CH6"], encoding='gb18030')

    plt.figure(figsize=(15, 10), dpi=80)
    plt.figure(1)

    plt.subplot(221)
    plt.plot(test_data['CH1(mV)'], label="Voltage")
    plt.grid(axis='y')
    plt.legend(loc=1)

    plt.subplot(222)
    plt.plot(test_data['CH4(mV)'], label="Current")
    plt.grid(axis='y')
    plt.legend(loc=1)

    plt.subplot(223)
    instance_power = [a * b for a, b in zip(test_data['CH1(mV)'], test_data['CH4(mV)'])]  # 瞬时功率
    plt.plot(instance_power, label="Instance_Power")
    plt.grid(axis='y')
    plt.legend(loc=1)

    plt.subplot(224)
    add_zero = [0.0] * 10
    instance_power = add_zero + instance_power + add_zero
    # instance_power = np.array(instance_power)
    count_power = []
    for i in range(9, len(instance_power) - 10):
        count_power.append(sum(instance_power[i - 10:i + 10]) / 20)
    plt.plot(count_power, label="Count_Power")
    # plt.plot(count_power[4800:5400])
    plt.grid(axis='y')
    plt.legend(loc=1)

    plt.tight_layout()
    plt.show()


def showData_5(data):
    # 尝试以20个数据(一个周期)为一段计算rms值，然后画出数据的曲线查看
    # 增添上取值的间隔step，查看变化程度
    csv_path_1 = "../data/吹风机-17.75-2.csv"
    test_data = pd.read_csv(csv_path_1, encoding='gb18030')
    # test_data = pd.read_csv(csv_path_1, names=["Time", "CH1", "CH2", "CH3", "CH4", "CH5", "CH6"], encoding='gb18030')

    step = 3

    plt.figure(figsize=(15, 10), dpi=80)
    plt.figure(1)

    plt.subplot(221)
    plt.plot(test_data['CH1(mV)'][::step], label="Voltage")
    plt.grid(axis='y')
    plt.legend(loc=1)

    plt.subplot(222)
    plt.plot(test_data['CH4(mV)'][::step], label="Current")
    plt.grid(axis='y')
    plt.legend(loc=1)

    plt.subplot(223)
    instance_power = [a * b for a, b in zip(test_data['CH1(mV)'][::step], test_data['CH4(mV)'][::step])]  # 瞬时功率
    plt.plot(instance_power, label="Instance_Power")
    plt.grid(axis='y')
    plt.legend(loc=1)

    plt.subplot(224)
    add_zero = [0.0] * 10
    # print(len())
    instance_power = add_zero + instance_power + add_zero
    # instance_power = np.array(instance_power)
    count_power = []
    for i in range(9, len(instance_power) - 10):
        count_power.append(sum(instance_power[i - 10:i + 10]) / 20)
    plt.plot(count_power, label="Count_Power")
    # plt.plot(count_power[4800:5400])
    plt.grid(axis='y')
    plt.legend(loc=1)

    plt.tight_layout()
    plt.show()


def showData_6(ax, cnt, j_file):
    # 画出fft变换后的频谱图
    with open(j_file) as file_obj:
        power_feature = json.load(file_obj)
    pf_fft_data = fft.fft(power_feature[cnt]["power_feature"])
    pf_ifft_data = fft.ifft(pf_fft_data)
    freqs = fft.fftfreq(500, 1 / 1000)
    ax.set_title(power_feature[cnt]["name"] + 'FFT变换,频谱图')
    # ax.set_label('Frequency 频率')
    # ax.set_ylabel('Power 功率')
    # plt.plot([i for i in range(4999)], pows[:10000][freqs > 0], c='orangered', label='Frequency')
    ax.plot(freqs[freqs > 0], np.abs(pf_fft_data)[freqs > 0], c='orangered', label='Frequency')

    # fig, axes = plt.subplots(9, 3)
    # cnt = 0
    # for i in range(9):
    #     for j in range(3):
    #         pf_fft_data = fft.fft(power_feature[cnt]["power_feature"])
    #         pf_ifft_data = fft.ifft(pf_fft_data)
    #         freqs = fft.fftfreq(500, 1 / 1000)
    #         axes[i][j].set_title(power_feature[cnt]["name"]+'FFT变换,频谱图')
    #         axes[i][j].set_xlabel('Frequency 频率')
    #         axes[i][j].set_ylabel('Power 功率')
    #         axes[i][j].plot(freqs[freqs > 0], np.abs(pf_fft_data)[freqs > 0], c='orangered', label='Frequency')
    #         cnt += 1
    # # fig.tight_layout()  # 调整整体空白
    # plt.show()
    # for i, pf_data in enumerate(power_feature):
    #     plt.subplot(9, 3, i + 1)
    #     pf_fft_data = fft.fft(pf_data["power_feature"])
    #     pf_ifft_data = fft.ifft(pf_fft_data)
    #     freqs = fft.fftfreq(500, 1 / 1000)
    #     plt.title(pf_data["name"]+'FFT变换,频谱图')
    #     plt.xlabel('Frequency 频率')
    #     plt.ylabel('Power 功率')
    #     # plt.plot([i for i in range(4999)], pows[:10000][freqs > 0], c='orangered', label='Frequency')
    #     plt.plot(freqs[freqs > 0], np.abs(pf_fft_data)[freqs > 0], c='orangered', label='Frequency')


def showData_7(data, frequency):
    rms_data = utils.power_data_process_rms(data, frequency)
    print(len(rms_data))
    plt.plot(rms_data)
    plt.show()


if __name__ == "__main__":
    # dataset_dir = 'CLEAN_REFIT_081116/'
    # csv_names = os.listdir(dataset_dir)
    # print(csv_names)
    #
    # csv_name = csv_names[0]
    # house_name = csv_name[:-4]
    csv_path = "../data/test-2021-12-14.csv"
    json_file = "../power_feature.json"
    # csv_path = "1.csv"
    # df = pd.read_csv(csv_path, encoding='gb18030')
    # # data = pd.read_csv(csv_path, names=["Time", "CH1", "CH2", "CH3", "CH4", "CH5", "CH6"], encoding='gb18030')
    #
    # showData_3(df)

    # 显示fft变换后的图
    # fig, axs = plt.subplots(3, 1, constrained_layout=True)
    # for i, ax in enumerate(axs.flat):
    #     showData_6(ax, i, json_file)
    # plt.show()

    row_data = pd.read_csv(csv_path, encoding="gb18030")
    showData_7(row_data[50000:100000], 1000)
