import copy
import math
import random
import time

import numpy as np
from scipy.stats import poisson
import readdata

# 读取数据 maps（地图包含poi点所需无人机架次），uavs（无人机路径坐标），poi_times（无人机在POI的拍摄时长）
maps, uavs, poi_times, poi_needs = readdata.get_data()
# 限制序列长度
budget_k = 25
# 数据整合
user_info = []
if len(uavs) != len(poi_times):
    print("Data Error")
for da in range(len(uavs)):
    user_info.append([uavs[da], poi_times[da], da])
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
        if len(s) == len(uavs):
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
        rand = random.randint(0, 1)
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
            indexs = uavs[s[i] - 1]
            poitim = poi_times[s[i] - 1]
            for j in range(len(indexs)):
                if map_.get(str(indexs[j]), 0) > 0:
                    values[i] += poitim[j]
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


if __name__ == '__main__':
    # 变量初始化——————————————————
    set_P = []  # 种群P初始化
    max_value = 0  # 记录序列最大值
    interval = 0  # 记录最大序列未发生变化间隙
    rond = 0  # 记录迭代轮次
    seq_max = []  # 记录最大序列
    value = 0  # 记录最大序列的值
    start = time.perf_counter()  # 记录开始时间
    inti = 0
    # 迭代开始————————————————————
    print("Start.....")
    while rond <= 100000:  # 当迭代超过100000时跳出迭代
        # 从种群中选出序列sl
        seq_s = []
        if len(set_P) != 0:
            seq_s = copy.deepcopy(random.choice(set_P))
        # 突变操作
        seq_s = mutation(seq_s)
        if len(seq_s) == 0 or len(seq_s) > (budget_k + 2):
            rond += 1
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
        print("has ran %d round.." % (rond + 1))
        # if len(seq_max) == 0:
        #     seq_max, value = get_max(set_P)
        # else:
        #     val = value_f(seq_s)
        #     if val > value and len(seq_s) <= budget_k:
        #         value = val
        #         seq_max = seq_s
        # rond += 1
        # # 变量更新
        # if value > max_value:
        #     max_value = value
        #     interval = 0
        #     print("value：", value)
        #     print("seq is：", seq_max)
        #     print("has ran %d round..\r\n" % (rond + 1))
        # else:
        #     interval += 1
    end = time.perf_counter()
    seq_max, max_value = get_max(set_P)
    print("set p :", set_P)
    print("the max value is :", max_value)
    print("max sequence is：", seq_max)
    print("sequence length is :", len(seq_max))
    print('spent time：', end - start)
    print("all round :", rond)
