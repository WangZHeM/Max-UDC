# 定义无人机变量
import copy
import math
import random
import numpy as np

uav_numbers = 500
poi_max = 3
map_width = 35
map_hight = 35
max_time = 100  # 无人机能量
poi_index = []
poi_uavned = []


# 地图生成
def generatemap(matrix, axis, val):
    randomx = axis[0] - 1
    randomy = axis[1] - 1
    cent = val
    matrix[randomx][randomy] = cent
    for i in range(cent):
        if randomx - i >= 0:
            if matrix[randomx - i][randomy] < val - i:
                matrix[randomx - i][randomy] = val - i
            tempi = 0
            j = i
            if randomy - i < 0:
                j = randomy
            while tempi <= j:
                if matrix[randomx - i][randomy - tempi] < val - i:
                    matrix[randomx - i][randomy - tempi] = val - i
                if matrix[randomx - i + tempi][randomy - j] < val - i:
                    matrix[randomx - i + tempi][randomy - j] = val - i
                tempi += 1
            tempi = 0
            j = i
            if randomy + i >= map_width:
                j = map_width - randomy - 1
            while tempi <= j:
                if matrix[randomx - i][randomy + tempi] < val - i:
                    matrix[randomx - i][randomy + tempi] = val - i
                if matrix[randomx - i + tempi][randomy + j] < val - i:
                    matrix[randomx - i + tempi][randomy + j] = val - i
                tempi += 1

        if randomx + i < map_hight:
            if matrix[randomx + i][randomy] < val - i:
                matrix[randomx + i][randomy] = val - i

            tempi = 0
            j = i
            if randomy - i < 0:
                j = randomy
            while tempi <= j:
                if matrix[randomx + i][randomy - tempi] < val - i:
                    matrix[randomx + i][randomy - tempi] = val - i
                if matrix[randomx + i - tempi][randomy - j] < val - i:
                    matrix[randomx + i - tempi][randomy - j] = val - i
                tempi += 1

            tempi = 0
            j = i
            if randomy + i >= map_width:
                j = map_width - randomy - 1
            while tempi <= j:
                if matrix[randomx + i][randomy + tempi] < val - i:
                    matrix[randomx + i][randomy + tempi] = val - i
                # print(randomy + j)
                if matrix[randomx + i - tempi][randomy + j] < val - i:
                    matrix[randomx + i - tempi][randomy + j] = val - i
                tempi += 1


# 用户数据
def generate_userdata(uav_num, pois):
    np.savetxt("Data/uavroute.txt", [], fmt="%d")
    np.savetxt("Data/uavusedtimes.txt", [], fmt="%d")
    ppos = copy.deepcopy(pois)
    for i in range(0, uav_num):
        # 设置用户经过的POI点个数
        # user_poiNum = random.randint(3, len(pois))
        user_poiNum = random.randint(30, 50)
        # 随机选取几个POI点
        # user_poi = copy.deepcopy(random.sample(pois, user_poiNum))
        user_pois = np.random.choice(np.array([num for num, p in enumerate(ppos)], dtype=object), size=user_poiNum,
                                     replace=True)

        uav_poi = []
        temp = []
        for ss in range(len(user_pois)):
            temp.append(copy.deepcopy(pois[user_pois[ss]]))

        # print(pois)
        for p in temp:
            while 1:
                randomx = random.randint(-poi_max + 1, poi_max - 1)
                randomy = random.randint(-poi_max + 1, poi_max - 1)
                p[0] = p[0] + randomx
                p[1] = p[1] + randomy
                if p[0] < 1:
                    p[0] = 1
                if p[0] > map_hight:
                    p[0] = map_hight
                if p[1] < 1:
                    p[1] = 1
                if p[1] > map_width:
                    p[1] = map_width
                if p not in uav_poi:
                    uav_poi.append(p)
                    break
        print(uav_poi)
        # 设置用户起点坐标
        user_index = random.choice(uav_poi)
        # 设置路径
        temp = copy.deepcopy(user_index)
        temp_poi = copy.deepcopy(uav_poi)
        times = 0
        while len(temp_poi) != 0:
            minx = 10000
            temppoiindex = None
            for t in range(len(temp_poi)):
                # 计算长度
                z = math.sqrt(math.fabs(temp_poi[t][0] - temp[0]) ** 2 + math.fabs(temp_poi[t][1] - temp[1]) ** 2)
                if minx > z:
                    minx = z
                    temppoiindex = t
            temp = temp_poi[temppoiindex]
            times += minx * 0.01
            del temp_poi[temppoiindex]

        uav_times = np.random.normal((max_time - times) / user_poiNum, scale=2, size=user_poiNum)
        uav_times = list(uav_times)
        for tt in range(len(uav_times)):
            if uav_times[tt] < 1:
                uav_times[tt] = 1
        with open('Data/uavroute.txt', 'a') as f1:
            np.savetxt(f1, uav_poi, delimiter=',', newline=' ', fmt='%d')
            f1.write('\n')
        f1.close()
        with open('Data/uavusedtimes.txt', 'a') as f2:
            np.savetxt(f2, uav_times, delimiter=',', newline=' ', fmt="%d")
            f2.write('\n')
        f2.close()


def creatInitdata():
    map = [[0 for i in range(map_width)] for j in range(map_hight)]
    # 生成POI
    pois = [[11, 7], [7, 20], [5, 31], [18, 20], [28, 16]]
    cent_ = poi_max
    for i in pois:
        generatemap(map, i, cent_)
    # print(poi_index)
    generate_userdata(uav_numbers, pois)
    np.savetxt("Data/map.txt", map, fmt="%d")


def choiceuavs(chionum):
    uavlist = [i for i in range(uav_numbers)]
    chiolist = np.random.choice(uavlist, chionum, replace=False)
    np.savetxt("Data/uavlist%d.txt" % chionum, chiolist, fmt="%d")


if __name__ == '__main__':
    creatInitdata()
    # choiceuavs(9)
