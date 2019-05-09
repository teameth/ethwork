import matplotlib.pyplot as plt
import networkx as nx
import numpy as np  
import pandas as pd
import os
from math import sqrt
from numpy import linalg as la

def DIaddfile(path,G):
	with open(path,'r',errors='ignore') as fg:
		count = 0
		for line in fg:
			count += 1
			if count == 1:
				continue
			info = line.strip().split(',')
			fromaddr = info[0]
			toaddr = info[1]
			if G.has_edge(fromaddr, toaddr):
				G[fromaddr][toaddr]['weight'] += 1
			else:
				G.add_edge(fromaddr, toaddr, weight = 1)
			#print fromaddr+' '+toaddr+' '+str(weight)
			# if fromaddr != toaddr:  #stop self cycle
			# 	pass#selfloop.append(fromaddr)
			# G.add_edge(fromaddr, toaddr, key= i, weight = weight)
			# i = i + 1
	fg.close()

if __name__ == "__main__":
	path_s = 'hashdata'
	files = os.listdir(path_s)
	G = nx.DiGraph()
	for file in files:
		# addfile(path_s+"/"+file, G)
		DIaddfile(path_s+"/"+file, G)
	writePath = 'trainCIG'
	fw = open(writePath, 'w')
	for u,v,d in G.edges(data = 'weight'):
		fw.write(u + ' ' + v + ' ' + str(d) + '\n')
	
