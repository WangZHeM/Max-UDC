import copy
import itertools
import math
import random
import time

import numpy as np
from scipy.stats import poisson
import readdata


def Init(uavlist, vark):
    global dirc, uav_route, spend_times, user_info, u_, budget_k
    # 读取数据 maps（地图包含poi点所需无人机架次），uav_route（无人机路径坐标），spend_times（无人机在POI的拍摄时长）
    # maps, uav_route, spend_times, poi_needs = readdata.get_data()
    maps = readdata.get_mapdata()
    uav_route_tmp = readdata.get_uavroute()
    spend_times_temp = readdata.get_spendtimes()
    uav_route = []
    spend_times = []
    for uav in uavlist:
        uav_route.append(uav_route_tmp[uav])
        spend_times.append(spend_times_temp[uav])
    # 限制序列长度
    budget_k = vark
    # 数据整合
    user_info = []
    if len(uav_route) != len(spend_times):
        print("Data Error")
    for da in range(len(uav_route)):
        user_info.append([uav_route[da], spend_times[da], da])
    u_ = [user_info[x][2] for x in range(len(user_info))]

    dirc = {}
    for x in range(len(maps)):
        for y in range(len(maps[0])):
            if maps[x][y] != 0:
                dirc[str([x + 1, y + 1])] = maps[x][y]


def get_value(s: list):
    if len(s) != 0:
        values = [0 for i in range(len(s))]
        map_ = copy.deepcopy(dirc)
        for i in range(len(s)):
            indexs = uav_route[s[i] - 1]
            poitim = spend_times[s[i] - 1]
            for j in range(len(indexs)):
                if map_.get(str(indexs[j]), 0) > 0:
                    values[i] += poitim[j]
                    map_[str(indexs[j])] -= 1
        return sum(values)
    else:
        return 0


def opt(uavlist, var_K):
    Init(uavlist, var_K)
    max_val = 0
    max_sqe = []
    start = time.perf_counter()
    for i in range(len(user_info)):
        temp = itertools.permutations(u_, i + 1)
        # print("the length = ", i + 1)
        for ss in temp:
            val = get_value(list(ss))
            if val > max_val and len(list(ss)) <= budget_k:
                max_val = val
                max_sqe = list(ss)
    end = time.perf_counter()

    # print("max_value = ", max_val)
    # print("max_sqe = ", max_sqe)
    # print("used time = ", end - start)
    return max_val

# opt(readdata.get_uavlist(9))
