def get_mapdata():
    with open("Data/map.txt", 'r') as f_map:
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
    return data_map


def get_uavroute():
    with open("Data/uavroute.txt", 'r') as f_uav:
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
    return data_uav


def get_uavdata():
    with open("Data/uavdata.txt", "r") as f_poi:
        pois = f_poi.readlines()
    uavdata = []
    for p in pois:
        p = p.strip("\n")
        p = p.rstrip()
        data_split = p.split(" ")
        temp = list(data_split)
        poi = []
        for i in temp:
            p = int(i)
            poi.append(p)
        uavdata.append(poi)
        # temp = list(map(list, data_split))
        # data_poi.append(temp[0])
    return uavdata


def get_spendtimes():
    with open("Data/uavusedtimes.txt", "r") as f_uavtimes:
        uavtime = f_uavtimes.readlines()
    spendtimes = []
    for o in uavtime:
        o = o.strip("\n")
        o = o.rstrip()
        data_split = o.split(" ")
        temp = list(data_split)
        uav=[]
        for i in temp:
            uav.append(int(i))
        spendtimes.append(uav)
    return spendtimes


def get_uavlist(num):
    with open("Data/uavlist%d.txt" % num, "r") as f_uavlist:
        uav_temp = f_uavlist.readlines()
    data_uavlist = []
    for uav in uav_temp:
        uav = uav.strip("\n")
        uav = uav.rstrip()
        data_uavlist.append(int(uav))
    return data_uavlist
