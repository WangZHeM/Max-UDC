# Experiment test
import time

import numpy as np

import Greedy
import creatdata
import readdata
import MaxUDC
import G_Greedy
import OPT

#Experiment 1-2
creatdata.choiceuavs(9)
uavset = readdata.get_uavlist(9)
value_MaxUDC, value_Ggreedy, value_Opt = 0, 0, 0
value_greedy = 0
spendtime_MaxUdc, spendtime_greedy, spendtime_opt_greedy = 0, 0, 0
bugK = 4
# Test 10 times
for i in range(10):
    start = time.perf_counter()
    uavs = np.random.choice(uavset, 7, replace=False)
    value_MaxUDC += MaxUDC.Max_UDC(uavs, bugK)[0]
    end1 = time.perf_counter()
    spendtime_MaxUdc += end1 - start
    value_Ggreedy += G_Greedy.G_Greedy(uavs, bugK)[0]
    end2 = time.perf_counter()
    spendtime_greedy += end2 - end1
    # value_Opt += OPT.opt(uavs, bugK)
    value_greedy += Greedy.greedy(uavs, bugK)[0]
    end3 = time.perf_counter()
    spendtime_opt_greedy += end3 - end2
print("the max value is:")
print("MaxUDC=", value_MaxUDC / 10, "Ggreedy=", value_Ggreedy / 10, "OPT=", value_Opt / 10)
print("spend time:")
print(spendtime_MaxUdc / 10, spendtime_greedy / 10, spendtime_opt_greedy / 10)

# Experiment 3-5
value_MaxUDC, value_Ggreedy, value_greedy = 0, 0, 0
len_MaxUDC, len_Ggreedy, len_greedy = 0, 0, 0
spendtime_MaxUdc, spendtime_Ggreedy, spendtime_greedy = 0, 0, 0
bugK = 25
# Test 3 times
testrond = 1
for i in range(testrond):
    start = time.perf_counter()
    uavs = np.random.choice([i for i in range(500)], 500, replace=False)
    value_MaxUDC += MaxUDC.Max_UDC(uavs, bugK)[0]
    len_MaxUDC += MaxUDC.Max_UDC(uavs, bugK)[1]
    end1 = time.perf_counter()
    spendtime_MaxUdc += end1 - start
    value_Ggreedy += G_Greedy.G_Greedy(uavs, bugK)[0]
    len_Ggreedy += G_Greedy.G_Greedy(uavs, bugK)[1]
    end2 = time.perf_counter()
    spendtime_Ggreedy += end2 - end1
    value_greedy += Greedy.greedy(uavs, bugK)[0]
    len_greedy += Greedy.greedy(uavs, bugK)[1]
    end3 = time.perf_counter()
    spendtime_greedy += end3 - end2
print("the max value is:")
print("MaxUDC =", value_MaxUDC / testrond, "Ggreedy =", value_Ggreedy / testrond, "Greedy =", value_greedy / testrond)
print("sequence length is:")
print("MaxUDC =", len_MaxUDC / testrond, "Ggreedy =", len_Ggreedy / testrond, "Greedy =", len_greedy / testrond)
print("spend time:")
print(spendtime_MaxUdc / testrond, spendtime_Ggreedy / testrond, spendtime_greedy / testrond)
