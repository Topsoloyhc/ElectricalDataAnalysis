import os
import numpy as np
import pandas as pd
import utils
import json

os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


if __name__ == "__main__":
    csv_file_1 = "../data/吹风机-17.75-2.csv"
    csv_file_2 = "../data/小电锅-19.75-2.csv"
    csv_file_3 = "../data/吸尘器-8.25-1.csv"
    csv_file_4 = "../data/热风机-11.75-1.csv"
    csv_file_5 = "../data/电熨斗-14.75-1.csv"
    csv_file_6 = "../data/鼓风机-11.5-1.csv"

    json_file = "../power_feature.json"

    count_power_1 = utils.power_data_process(csv_file_1)
    count_power_2 = utils.power_data_process(csv_file_2)
    count_power_3 = utils.power_data_process(csv_file_3)
    count_power_4 = utils.power_data_process(csv_file_4)
    count_power_5 = utils.power_data_process(csv_file_5)
    count_power_6 = utils.power_data_process(csv_file_6)

    s_0 = count_power_1[0:500]  # 无电器运行时

    '''吹风机
        0-1：1750-2250
    
        1-2：4600-5100
        
        2-1：7480-7980
        
        1-0：10050-10550
        
        0-2：12800-13300
        
        2-0：16570-17070
        
        1：2500-3000
        
        2：6000-6500
    '''
    s_1_0_1 = count_power_1[1750:2250]
    s_1_1_2 = count_power_1[4600:5100]
    s_1_2_1 = count_power_1[7480:7980]
    s_1_1_0 = count_power_1[10050:10550]
    s_1_0_2 = count_power_1[12800:13300]
    s_1_2_0 = count_power_1[16570:17070]
    s_1_1 = count_power_1[2500:3000]
    s_1_2 = count_power_1[6000:6500]

    ''' 小电锅
        0-1：2900-3400
    
        1-0：8740-9240
        
        0-2：12330-12830
        
        2-0：17690-18190
        
        1：5000-5500
        
        2：13000-13500
    '''
    s_2_0_1 = count_power_2[2900:3400]
    s_2_1_0 = count_power_2[8740:9240]
    s_2_0_2 = count_power_2[12330:12830]
    s_2_2_0 = count_power_2[17690:18190]
    s_2_1 = count_power_2[5000:5500]
    s_2_2 = count_power_2[13000:13500]

    ''' 吸尘器
        0-1：2450-2950 Δt = 500
    
        1-0：6380-6880
        
        1：5000-5500
    '''
    s_3_0_1 = count_power_3[2450:2950]
    s_3_1_0 = count_power_3[6380:6880]
    s_3_1 = count_power_3[5000:5500]

    ''' 热风机
        0-1：2625-3125

        1-0：10420-10920
            
        1：5000-5500
    '''
    s_4_0_1 = count_power_4[2625:3125]
    s_4_1_0 = count_power_4[10420:10920]
    s_4_1 = count_power_4[5000:5500]

    ''' 电熨斗
        0-1：4470-4970
        
        1-0：12010-12510
        
        1：8000-8500
    '''
    s_5_0_1 = count_power_5[4470:4970]
    s_5_1_0 = count_power_5[12010:12510]
    s_5_1 = count_power_5[8000:8500]

    ''' 鼓风机
        0-1：2900-3400 Δt = 500
        
        1-0：9150-9650
        
        1：6000-6500
    '''
    s_6_0_1 = count_power_6[2900:3400]
    s_6_1_0 = count_power_6[9150:9650]
    s_6_1 = count_power_6[6000:6500]

    record = [{"name": "无电器运行",
               "label": 0,
               "type": 1,  # 0暂态，1稳态
               "power_feature": s_0,
               },
              {"name": "吹风机0-1档",
               "label": 1,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_1_0_1,
               },
              {"name": "吹风机1-2档",
               "label": 2,
               "type": 0,
               "power_feature": s_1_1_2,
               },
              {"name": "吹风机2-1档",
               "label": 3,
               "type": 0,
               "power_feature": s_1_2_1,
               },
              {"name": "吹风机1-0档",
               "label": 4,
               "type": 0,
               "power_feature": s_1_1_0,
               },
              {"name": "吹风机0-2档",
               "label": 5,
               "type": 0,
               "power_feature": s_1_0_2,
               },
              {"name": "吹风机2-0档",
               "label": 6,
               "type": 0,
               "power_feature": s_1_2_0,
               },
              {"name": "吹风机  1档",
               "label": 7,
               "type": 1,
               "power_feature": s_1_1,
               },
              {"name": "吹风机  2档",
               "label": 8,
               "type": 1,  # 0暂态，1稳态
               "power_feature": s_1_2,
               },
              {"name": "小电锅0-1档",
               "label": 9,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_2_0_1,
               },
              {"name": "小电锅1-0档",
               "label": 10,
               "type": 0,
               "power_feature": s_2_1_0,
               },
              {"name": "小电锅0-2档",
               "label": 11,
               "type": 0,
               "power_feature": s_2_0_2,
               },
              {"name": "小电锅2-0档",
               "label": 12,
               "type": 0,
               "power_feature": s_2_2_0,
               },
              {"name": "小电锅  1档",
               "label": 13,
               "type": 1,
               "power_feature": s_2_1,
               },
              {"name": "小电锅  2档",
               "label": 14,
               "type": 1,  # 0暂态，1稳态
               "power_feature": s_2_2,
               },
              {"name": "吸尘器0-1档",
               "label": 15,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_3_0_1,
               },
              {"name": "吸尘器1-0档",
               "label": 16,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_3_0_1,
               },
              {"name": "吸尘器  1档",
               "label": 17,
               "type": 1,
               "power_feature": s_3_1,
               },
              {"name": "热风机0-1档",
               "label": 18,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_4_0_1,
               },
              {"name": "热风机1-0档",
               "label": 19,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_4_0_1,
               },
              {"name": "热风机  1档",
               "label": 20,
               "type": 1,
               "power_feature": s_4_1,
               },
              {"name": "电熨斗0-1档",
               "label": 21,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_5_0_1,
               },
              {"name": "电熨斗1-0档",
               "label": 22,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_5_0_1,
               },
              {"name": "电熨斗  1档",
               "label": 23,
               "type": 1,
               "power_feature": s_5_1,
               },
              {"name": "鼓风机0-1档",
               "label": 24,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_6_0_1,
               },
              {"name": "鼓风机1-0档",
               "label": 25,
               "type": 0,  # 0暂态，1稳态
               "power_feature": s_6_0_1,
               },
              {"name": "鼓风机  1档",
               "label": 26,
               "type": 1,
               "power_feature": s_6_1,
               },
              ]
    # print(record[0]["label"])
    with open(json_file, 'w') as file_obj:
        json.dump(record, file_obj)
