import copy
import math
import time

import numpy as np

import readdata

# 读取数据 maps（地图大小），uavs（无人机拍摄时间数据），poi_times（POI点所需无人机数量）
maps, uavs, poi_times, poi_needs = readdata.get_data()
# 限制序列长度
budget_k = 25
# 种群P
set_p = []
# 数据整合
user_info = []
if len(uavs) != len(poi_times):
    print("Data Error")
for da in range(len(uavs)):
    user_info.append([uavs[da], poi_times[da], da])
dirc = {}
for x in range(len(maps)):
    for y in range(len(maps[0])):
        if maps[x][y] != 0:
            dirc[str([x + 1, y + 1])] = maps[x][y]


# 目标函数f
def value_f(s: list):
    if len(s) != 0:
        values = [0 for i in range(len(s))]
        map_ = copy.deepcopy(dirc)
        for i in range(len(s)):
            indexs = uavs[s[i] - 1]
            poitim = poi_times[s[i] - 1]
            for j in range(len(indexs)):
                if map_.get(str(indexs[j]), 0) > 0:
                    values[i] += poitim[j]
                    map_[str(indexs[j])] -= 1
        return sum(values)
    else:
        return 0


if __name__ == '__main__':
    # 初始化
    cp_uav = copy.deepcopy(user_info)
    seqs = []
    max_ = 0
    print("start")
    cp_seqs = []  # 待插入序列
    start = time.perf_counter()  # 记录开始时间
    # 迭代
    while len(seqs) < budget_k:  # 当序列s长度小于15时
        # 从种群集合中选出能使目标函数值最大的序列
        max_s = []
        for i in range(len(uavs)):
            cp_seqs = copy.deepcopy(seqs)
            # 排除重复元素
            if i in cp_seqs:
                continue
            cp_seqs.insert(len(cp_seqs), i)
            # 记录最大值
            if value_f(cp_seqs) > value_f(max_s):
                max_s = copy.deepcopy(cp_seqs)
        val = value_f(max_s)
        if val > max_:
            max_ = val
            seqs = copy.deepcopy(max_s)
        else:
            break
        print("round end")
        print("sets length is ", len(seqs))
        print("value is ", max_)
        print("____________________________")
    end = time.perf_counter()
    print("max value:", max_)
    print("max sequence:", seqs)
    print("max length:", len(seqs))
    print('spent time：', end - start)
