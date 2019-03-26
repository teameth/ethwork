#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE

def nametoVecDict(filepath):
    labelMat = []
    disMat = []
    vector = []
    fr = open(filepath, 'rb')
    for line in fr.readlines():
        lineArr = line.strip().split()
        disMat = []
        for k in range(1, lineArr.__len__()):
            disMat.append(float(lineArr[k]))
        labelMat.append(str(lineArr[0], encoding = "utf-8"))
        vector.append(disMat)
    fr.close()
    find = dict(zip(labelMat, vector))
    return labelMat,find

def readLabel(filepath, k):
	key=[]
	need_name = pd.read_csv(filepath, header = None)
	key = need_name[k].tolist()
	return key

def nametoType(filepath):
	fr = open(filepath, 'rb')
	accountDict = {}
	accountList = []
	accountType = []
	for accountLine in fr.readlines():
		Aline = str(accountLine, encoding = "utf-8")
		DictLineArr = Aline.strip().split(',')
		accountList.append(str(DictLineArr[1]))
		accountType.append(str(DictLineArr[2]))
	accountDict = dict(zip(accountList, accountType))
	return accountDict

if __name__ == '__main__':
	print("1")
	vecpath = '20line'
	address, findVec = nametoVecDict(vecpath)
	print("2")
	key = readLabel('labellist.csv', 0)
	print("3")
	accountDict = nametoType('newestlands')
	vec = []
	names = []
	result = []
	sortMat = []
	count = 0
	print("4")
	data = []
	'''
	for i in key:
		a1 = np.array(findVec.get(i))
		fr2 = open(vecpath, 'rb')
		print(i)
		data.clear()
		result.clear()
		sortMat.clear()
		for line in fr2.readlines():
			count=count+1
			lineArr=line.strip().split()
			data.clear()
			for k in range(1, lineArr.__len__()):
				data.append(float(lineArr[k]))
			label = (str(lineArr[0], encoding = "utf-8"))
			a2 = np.array(data)
			dist = np.linalg.norm(a2 - a1)
			distout=str(dist)
			sortMat.append((dist,label))
		result = sorted(sortMat)
		print(type(result))
		for k in range(1200):
			if k < len(result):
				if str(result[k][1]) in names:
					continue
				else:
					names.append(str(result[k][1]))
					vec.append(findVec.get(str(result[k][1])))

	fw = open('/Users/mark/Desktop/result.txt', 'w')
	fw.write(str(names.__len__()))
	for name in names:
		fw.write(name + '\n')
	'''
	print("5")
	fw = open('ImportantResult.txt', 'r')
	count = 0
	for line in fw.readlines():
		line = line.strip()
		if count>0:
			if line in findVec.keys():
				names.append(line)
				vec.append(findVec.get(line))
		else:
			count+=1
	fw.close()
	for i in range(90000):
		ran = random.randint(0, address.__len__() - 1)
		if address[ran] in names:
			continue
		names.append(address[ran])
		vec.append(findVec.get(address[ran]))
#		fw.write(str(ran) + '\n')
	print("6")
	node_color = []
	node_size = []
	# 画图
	for line in names:
		if line in key:
			node_color.append('r')
			node_size.append(int(45))
		elif accountDict.get(line)=='Sc':
			node_color.append('g')
			node_size.append(int(5))
		elif accountDict.get(line)=='No':
			node_color.append('b')
			node_size.append(int(5))

	types = ['random','pca']
	start_time = time.time()
	name2tsne_vec = {}

	for type in types:
#        , learning_rate = 120
		print("7")
		two_dim_vec = TSNE(n_components=2, init=type, perplexity = 10, early_exaggeration = 36).fit_transform(vec)
		name2tsne_vec = dict(zip(names, two_dim_vec))
		dim_vec_path = type+' tsneResult.txt'
		fout = open(dim_vec_path,'w')
		for label,value in name2tsne_vec.items():
			fout.write(label+':'+str(value)+'\n')
		print("8")
		plt.figure(figsize=(50,20))
		plt.scatter(two_dim_vec[:, 0], two_dim_vec[:, 1], s = node_size, c = node_color)
		plt.savefig('fig '+ type +'.png')
		# plt.show()
	print('tSNE done, elapsed time: {}'.format(round(time.time()-start_time)))
