import copy
import math
import random
import time

import numpy as np

import creatdata
import readdata


def Init(uavlist, varK):
    global maps, uav_route, spend_times, u_, dirc, budget_k
    # 读取数据 maps（地图包含poi点所需无人机架次），uav_route（无人机路径坐标），spend_times（无人机在POI的拍摄时长）
    maps = readdata.get_mapdata()
    uav_route_tmp = readdata.get_uavroute()
    spend_times_temp = readdata.get_spendtimes()
    uav_route = []
    spend_times = []
    for uav in uavlist:
        uav_route.append(uav_route_tmp[uav])
        spend_times.append(spend_times_temp[uav])
    # 限制序列长度
    budget_k = varK
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


# 删除操作
def deletion(s: list):
    # 选取删除序列
    rand_del = random.randint(0, len(s) - 1)
    del s[rand_del]
    return s


# 插入操作
def insertion(s):
    temps = copy.deepcopy(u_)
    while 1:
        # 选取插入序列
        if len(s) == len(uav_route):
            break
        rand_insert = random.randint(0, len(temps) - 1)
        # rand_insert = random.choice(temps)
        # 判断是否重复
        if temps[rand_insert] not in s:
            s.insert(random.randint(0, len(s)), temps[rand_insert])
            break
        else:
            del temps[rand_insert]

    return s


# 突变器
def mutation(s):
    # 利用泊松分布确定突变次数
    for r in range(np.random.poisson(1)):
        # 均匀分布确定操作，rand=0（删除操作），rand=1（插入操作）
        # rand = random.randint(0, 1)
        rand = np.random.choice([0, 1], 1)
        if rand == 0:
            # 删除操作
            if len(s) != 0:
                s = deletion(s)
        else:
            # 插入操作
            s = insertion(s)
    return s


# 目标函数f
def value_f(s: list):
    if len(s) != 0:
        values = [0 for i in range(len(s))]
        map_ = copy.deepcopy(dirc)
        for i in range(len(s)):
            indexs = uav_route[s[i] - 1]
            poitim = spend_times[s[i] - 1]
            for j in range(len(indexs)):
                if map_.get(str(indexs[j]), 0) > 0:
                    values[i] += poitim[j]
                    # values[i] += math.sqrt(poitim[j])
                    map_[str(indexs[j])] -= 1
        return sum(values)
    else:
        return 0


# f1函数，当序列长度
def value_f1(s: list):
    # 淘汰序列长度大于2k的序列
    if len(s) >= budget_k * 2:
        return -1000000
    else:
        return value_f(s)


# 占优计算，比较序列s与序列s_的占优度， do=0 （不可比） do=1 （弱占优） do=2 （强占优）
def domination(s: list, s_: list):
    weakly_do = False
    do = 0
    val1 = value_f1(s)
    val1_ = value_f1(s_)
    # 弱占优比较
    if val1 >= val1_ and len(s) <= len(s_):
        weakly_do = True
        do = 1
    # 强占优比较
    if weakly_do:
        if val1 > val1_ or len(s) < len(s_):
            do = 2
    return do


# 计算最大序列
def get_max(P: list):
    max_ = 0
    max_seq = []
    # 寻找长度限制下的最大序列
    # max_seq = copy.deepcopy(P[0])
    for p in range(len(P)):
        if len(P[p]) > budget_k:
            continue
        val = value_f(P[p])
        if val == max_ and len(P[p]) < len(max_seq):
            max_ = val
            max_seq = P[p]
        if val > max_:
            max_ = val
            max_seq = P[p]
    return max_seq, max_


def Max_UDC(uavlist, var_K):
    # 变量初始化——————————————————
    Init(uavlist, var_K)
    set_P = []  # 种群P初始化
    # max_value = 0  # 记录序列最大值
    # interval = 0  # 记录最大序列未发生变化间隙
    rond = 0  # 记录迭代轮次
    # seq_max = []  # 记录最大序列
    # value = 0  # 记录最大序列的值
    start = time.perf_counter()  # 记录开始时间
    # inti = 0
    # 迭代开始————————————————————
    # print("Start.....")
    while rond <= math.log(len(uavlist)) * 20000:  # 当迭代超过100000时跳出迭代
        # 从种群中选出序列sl
        seq_s = []
        if len(set_P) != 0:
            seq_s = copy.deepcopy(random.choice(set_P))
        # 突变操作
        seq_s = mutation(seq_s)
        if len(seq_s) == 0:
            # rond += 1
            continue
        # 将序列s插入到种群P中
        do_flag = True  # 种群中是否存在强占优序列的标识符
        dele_ind = -1
        for p in range(len(set_P)):
            if len(set_P[p]) == len(seq_s):
                d1 = domination(seq_s, set_P[p])
                if d1 >= 1:
                    dele_ind = p
                else:
                    do_flag = False
        if do_flag:
            if dele_ind != -1:
                del set_P[dele_ind]
            # 将序列s加入种群P
            # if len(seq_s) <= (2 * budget_k):
            #     set_P.append(seq_s)
            set_P.append(seq_s)
        rond += 1
        # print("has ran %d round.." % (rond + 1))
    end = time.perf_counter()
    seq_max, max_value = get_max(set_P)
    # print("set p :", set_P)
    # print("the max value is :", max_value)
    # print("max sequence is：", [uavlist[seq_max[i]] for i in range(len(seq_max))])
    # print("sequence length is :", len(seq_max))
    # print('spent time：', end - start)
    # print("all round :", rond)
    return max_value, len(seq_max)
