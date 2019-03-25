#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
labelMat = []
fr = open('dwMFG', 'rb')
#读取每一个向量的名字（6位）
for line in fr.readlines():
    lineArr = line.split()
    L = lineArr[0]
    name = str(L)
    labelMat.append(name)
    # print(labelMat)
fr.close()

disMat=[]
vector = []
fr1 = open('dwMFG', 'rb')
for line in fr1.readlines():
    lineArr=line.strip().split()
    disMat=([float(lineArr[1]),float(lineArr[2]),float(lineArr[3]),float(lineArr[4]),float(lineArr[5]),float(lineArr[6]),float(lineArr[7]),float(lineArr[8]),float(lineArr[9]),float(lineArr[10]),float(lineArr[11]),float(lineArr[12]),float(lineArr[13]),float(lineArr[14]),float(lineArr[15]),float(lineArr[16]),float(lineArr[17]),float(lineArr[18]),float(lineArr[19]),float(lineArr[20]),float(lineArr[21]),float(lineArr[22]),float(lineArr[23]),float(lineArr[24]),float(lineArr[25]),float(lineArr[26]),float(lineArr[27]),float(lineArr[28]),float(lineArr[29]),float(lineArr[30]),float(lineArr[31]),float(lineArr[32]),float(lineArr[33]),float(lineArr[34]),float(lineArr[35]),float(lineArr[36]),float(lineArr[37]),float(lineArr[38]),float(lineArr[39]),float(lineArr[40]),float(lineArr[41]),float(lineArr[42]),float(lineArr[43]),float(lineArr[44]),float(lineArr[45]),float(lineArr[46]),float(lineArr[47]),float(lineArr[48]),float(lineArr[49]),float(lineArr[50]),float(lineArr[51]),float(lineArr[52]),float(lineArr[53]),float(lineArr[54]),float(lineArr[55]),float(lineArr[56]),float(lineArr[57]),float(lineArr[58]),float(lineArr[59]),float(lineArr[60]),float(lineArr[61]),float(lineArr[62]),float(lineArr[63]),float(lineArr[64]),float(lineArr[65]),float(lineArr[66]),float(lineArr[67]),float(lineArr[68]),float(lineArr[69]),float(lineArr[70]),float(lineArr[71]),float(lineArr[72]),float(lineArr[73]),float(lineArr[74]),float(lineArr[75]),float(lineArr[76]),float(lineArr[77]),float(lineArr[78]),float(lineArr[79]),float(lineArr[80]),float(lineArr[81]),float(lineArr[82]),float(lineArr[83]),float(lineArr[84]),float(lineArr[85]),float(lineArr[86]),float(lineArr[87]),float(lineArr[88]),float(lineArr[89]),float(lineArr[90]),float(lineArr[91]),float(lineArr[92]),float(lineArr[93]),float(lineArr[94]),float(lineArr[95]),float(lineArr[96]),float(lineArr[97]),float(lineArr[98]),float(lineArr[99]),float(lineArr[100]),float(lineArr[101]),float(lineArr[102]),float(lineArr[103]),float(lineArr[104]),float(lineArr[105]),float(lineArr[106]),float(lineArr[107]),float(lineArr[108]),float(lineArr[109]),float(lineArr[110]),float(lineArr[111]),float(lineArr[112]),float(lineArr[113]),float(lineArr[114]),float(lineArr[115]),float(lineArr[116]),float(lineArr[117]),float(lineArr[118]),float(lineArr[119]),float(lineArr[120]),float(lineArr[121]),float(lineArr[122]),float(lineArr[123]),float(lineArr[124]),float(lineArr[125]),float(lineArr[126]),float(lineArr[127]),float(lineArr[128])])
    # a1 = np.array(disMat)
    # print(disMat)
    vector.append(disMat)
    # print(vector)
    # print(type(vector))
fr1.close()
#生成字典
find = dict(zip(labelMat, vector))
# print(dict)

need_name = pd.read_excel('labellist.xlsx', header = None)
# print(type(need_name))
# print(need_name.icol[0])
key = need_name[0].tolist()
# print(type(key))
# print(key)

label = []
data = []
count = 1
sortMat = []
result = []
fr3 = open('newestlands', 'rb')
accountDict = {}
accountList = []
accountType = []
for accountLine in fr3.readlines():
    Aline = str(accountLine)
    DictLineArr = Aline.strip().split(',')
    
    accountList.append(str(DictLineArr[1]))
    accountType.append(str(DictLineArr[2]))
accountDict = dict(zip(accountList, accountType))
for i in key:
    #print(i)
    #a3=find.get(i)
    #print (a3)
    a1 = np.array(find.get(i))
    fr2 = open('dwMFG', 'rb')
    print(i)
    result=[]
    sortMat=[]
    for line in fr2.readlines():
        count=count+1
        lineArr=line.strip().split()
        data=([float(lineArr[1]),float(lineArr[2]),float(lineArr[3]),float(lineArr[4]),float(lineArr[5]),float(lineArr[6]),float(lineArr[7]),float(lineArr[8]),float(lineArr[9]),float(lineArr[10]),float(lineArr[11]),float(lineArr[12]),float(lineArr[13]),float(lineArr[14]),float(lineArr[15]),float(lineArr[16]),float(lineArr[17]),float(lineArr[18]),float(lineArr[19]),float(lineArr[20]),float(lineArr[21]),float(lineArr[22]),float(lineArr[23]),float(lineArr[24]),float(lineArr[25]),float(lineArr[26]),float(lineArr[27]),float(lineArr[28]),float(lineArr[29]),float(lineArr[30]),float(lineArr[31]),float(lineArr[32]),float(lineArr[33]),float(lineArr[34]),float(lineArr[35]),float(lineArr[36]),float(lineArr[37]),float(lineArr[38]),float(lineArr[39]),float(lineArr[40]),float(lineArr[41]),float(lineArr[42]),float(lineArr[43]),float(lineArr[44]),float(lineArr[45]),float(lineArr[46]),float(lineArr[47]),float(lineArr[48]),float(lineArr[49]),float(lineArr[50]),float(lineArr[51]),float(lineArr[52]),float(lineArr[53]),float(lineArr[54]),float(lineArr[55]),float(lineArr[56]),float(lineArr[57]),float(lineArr[58]),float(lineArr[59]),float(lineArr[60]),float(lineArr[61]),float(lineArr[62]),float(lineArr[63]),float(lineArr[64]),float(lineArr[65]),float(lineArr[66]),float(lineArr[67]),float(lineArr[68]),float(lineArr[69]),float(lineArr[70]),float(lineArr[71]),float(lineArr[72]),float(lineArr[73]),float(lineArr[74]),float(lineArr[75]),float(lineArr[76]),float(lineArr[77]),float(lineArr[78]),float(lineArr[79]),float(lineArr[80]),float(lineArr[81]),float(lineArr[82]),float(lineArr[83]),float(lineArr[84]),float(lineArr[85]),float(lineArr[86]),float(lineArr[87]),float(lineArr[88]),float(lineArr[89]),float(lineArr[90]),float(lineArr[91]),float(lineArr[92]),float(lineArr[93]),float(lineArr[94]),float(lineArr[95]),float(lineArr[96]),float(lineArr[97]),float(lineArr[98]),float(lineArr[99]),float(lineArr[100]),float(lineArr[101]),float(lineArr[102]),float(lineArr[103]),float(lineArr[104]),float(lineArr[105]),float(lineArr[106]),float(lineArr[107]),float(lineArr[108]),float(lineArr[109]),float(lineArr[110]),float(lineArr[111]),float(lineArr[112]),float(lineArr[113]),float(lineArr[114]),float(lineArr[115]),float(lineArr[116]),float(lineArr[117]),float(lineArr[118]),float(lineArr[119]),float(lineArr[120]),float(lineArr[121]),float(lineArr[122]),float(lineArr[123]),float(lineArr[124]),float(lineArr[125]),float(lineArr[126]),float(lineArr[127]),float(lineArr[128])])
        label=(str(lineArr[0]))
        a2 = np.array(data)
        #print (a1)
        #print (a2)
        dist = np.linalg.norm(a2 - a1)
        distout=str(dist)
        if dist<20:
            sortMat.append((dist,label))
    result = sorted(sortMat)
    print(type(result))
    path = i
    f = open(path,'w')
    for k in range(200 if len(result)>200 else len(result)):
        if k < len(result):
            if accountDict.get(result[k][1]) == 'No':
                f.write(str(result[k][0]) + ' ' + str(result[k][1]) + '\n')
            # f.write('\n')
    # print('result')
    # print(count)
    # print(result)
