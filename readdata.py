import numpy as np


def get_data():
    with open("./map.txt", 'r') as f_map:
        maps_ = f_map.readlines()
    data_map = []
    for map_ in maps_:
        map_ = map_.strip("\n")
        data_split = map_.split(",")
        temp = list(data_split)
        poi = []
        for i in temp:
            p = i.split(" ")
            poi = list(map(int, p))
        data_map.append(poi)

    with open("./userpoi.txt", 'r') as f_uav:
        uavs_ = f_uav.readlines()
    data_uav = []
    for u in uavs_:
        datas = []
        u = u.strip("\n")
        u = u.rstrip()
        data_split = u.split(" ")
        temp = list(data_split)
        for i in temp:
            ua = i.split(",")
            uav = [int(ua[0]), int(ua[1])]
            datas.append(uav)
        data_uav.append(datas)

    with open("./usertimes.txt", "r") as f_poi:
        pois = f_poi.readlines()
    data_poi = []
    for p in pois:
        p = p.strip("\n")
        p = p.rstrip()
        data_split = p.split(" ")
        temp = list(data_split)
        poi = []
        for i in temp:
            p = int(i)
            poi.append(p)
        data_poi.append(poi)
        # temp = list(map(list, data_split))
        # data_poi.append(temp[0])

    with open("./poitimes.txt", "r") as f_poitimes:
        poitime = f_poitimes.readlines()
    poitimes = []
    for o in poitime:
        o = o.strip("\n")
        o = o.rstrip()
        data_split = o.split(" ")
        temp = list(data_split)
        for i in temp:
            poitimes.append(int(i))
    return data_map, data_uav, data_poi, poitimes
