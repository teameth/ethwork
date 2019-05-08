"""
Clustering Evaluation: Conductance
Author: Liu Yang
Date: 2019-5-8
"""

import csv
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import operator
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class Graph(object):
    def __init__(self):
        self.G = None
        self.look_up_dict = {}
        self.look_back_list = []
        self.node_size = 0

    def encode_node(self):
        look_up = self.look_up_dict
        look_back = self.look_back_list
        for node in self.G.nodes():
            look_up[node] = self.node_size
            look_back.append(node)
            self.node_size += 1
            self.G.nodes[node]['status'] = ''

    def read_g(self, g):
        self.G = g
        self.encode_node()

    def read_adjlist(self, filename):
        """ Read graph from adjacency file in which the edge must be unweighted
            the format of each line: v1 n1 n2 n3 ... nk
            :param filename: the filename of input file
        """
        self.G = nx.read_adjlist(filename, create_using=nx.DiGraph())
        for i, j in self.G.edges():
            self.G[i][j]['weight'] = 1.0
        self.encode_node()

    def read_edgelist(self, filename, weighted=False, directed=False):
        self.G = nx.DiGraph()

        if directed:
            def read_unweighted(l):
                src, dst = l.split()
                self.G.add_edge(src, dst)
                self.G[src][dst]['weight'] = 1.0

            def read_weighted(l):
                src, dst, w = l.split()
                self.G.add_edge(src, dst)
                self.G[src][dst]['weight'] = float(w)
        else:
            def read_unweighted(l):
                src, dst = l.split()
                self.G.add_edge(src, dst)
                self.G.add_edge(dst, src)
                self.G[src][dst]['weight'] = 1.0
                self.G[dst][src]['weight'] = 1.0

            def read_weighted(l):
                src, dst, w = l.split()
                self.G.add_edge(src, dst)
                self.G.add_edge(dst, src)
                self.G[src][dst]['weight'] = float(w)
                self.G[dst][src]['weight'] = float(w)
        fin = open(filename, 'r')
        func = read_unweighted
        if weighted:
            func = read_weighted
        while 1:
            l = fin.readline()
            if l == '':
                break
            func(l)
        fin.close()
        self.encode_node()

    def read_node_label(self, filename):
        fin = open(filename, 'r')
        while 1:
            l = fin.readline()
            if l == '':
                break
            vec = l.split()
            self.G.nodes[vec[0]]['label'] = vec[1:]
        fin.close()

    def read_node_features(self, filename):
        fin = open(filename, 'r')
        for l in fin.readlines():
            vec = l.split()
            self.G.nodes[vec[0]]['feature'] = np.array(
                [float(x) for x in vec[1:]])
        fin.close()

    def read_node_status(self, filename):
        fin = open(filename, 'r')
        while 1:
            l = fin.readline()
            if l == '':
                break
            vec = l.split()
            self.G.nodes[vec[0]]['status'] = vec[1]  # train test valid
        fin.close()

    def read_node_role(self, filename):
        fin = open(filename, 'r')
        while 1:
            l = fin.readline()
            if l == '':
                break
            eoa, sc, w = l.split()
            self.G.nodes[eoa]['role'] = 'eoa'
            self.G.nodes[sc]['role'] = 'sc'            
        fin.close()

    def read_edge_label(self, filename):
        fin = open(filename, 'r')
        while 1:
            l = fin.readline()
            if l == '':
                break
            vec = l.split()
            self.G[vec[0]][vec[1]]['label'] = vec[2:]
        fin.close()



def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('--input', required=True,
                        help='Input graph file')
    parser.add_argument('--graph_type', default='CIG', choices=['MFG', 'CIG', 'CCG'],
                        help='Input graph type')
    parser.add_argument('--graph_format', default='edgelist', choices=['adjlist', 'edgelist'],
                        help='Input graph format')
    parser.add_argument('--cluster',
                        help='Clustering result file')
    parser.add_argument('--directed', action='store_true',
                        help='Treat graph as directed.')
    parser.add_argument('--figure', default='',
                        help='The file of node label')
    parser.add_argument('--feature_file', default='',
                        help='The file of node features')
    parser.add_argument('--weighted', action='store_true',
                        help='Treat graph as weighted')
    args = parser.parse_args()
    return args


def read_labeled_account(filename):
    label = {}
    with open(filename, 'r') as labelfile:
        exchange_account = csv.reader(labelfile)
        for notes, address in exchange_account:
            label[address] = str(notes)
    return label.keys()


def read_cluster(filename):
    cluster = {}
    with open(filename, 'r') as clusterfile:
        clusterLines = clusterfile.readlines()
    for line in clusterLines:
        center_id, cluster_id = line.strip().split('\t')
        clusterList = cluster_id.split(',')
        cluster[int(center_id)] = clusterList
    return cluster


def get_top_k_candidates(targetList, k, labelList, outPath=None):
    top_k_list = targetList[:k]
    top_k_dict = dict(top_k_list)  # key is address str, value is degree
    top_k_set = set(top_k_dict.keys())
    right_set = top_k_set & set(labelList)
    print("Precision@{}: {}".format(k, len(right_set)/k))
    print("Recall@{}: {}".format(k, len(right_set)/len(labelList)))    
    if outPath:
        f_r = open('degree_top{}'.format(k), 'w')
        for t in top_k_dict.items():
            f_r.write(t[0]+'\t'+str(t[1])+'\n')
        f_r.close()

def plot_degree(G, save_path=None):
    matplotlib.use('Agg')
    degrees = G.degree() # Return a 2-tuple list
    # degrees_w = G.degree(weight='weight') 
    degreesDict = dict(degrees)
    degreesValue = sorted(set(degreesDict.values())) # Remove duplicate, default ascending order
    degreesCount = [list(degreesDict.values()).count(x) for x in degreesValue]
    plt.loglog(degreesValue, degreesCount, 'r.') 
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    if save_path:
        plt.savefig(save_path)



if __name__ == "__main__":
    args = parse_args()
    GG = nx.lollipop_graph(4, 6)
    print(GG.degree())
    g = Graph()
    start_time = time.time()
    if args.graph_format == 'adjlist':
        g.read_adjlist(filename=args.input)
    elif args.graph_format == 'edgelist':
        g.read_edgelist(filename=args.input, weighted=args.weighted,
                        directed=args.directed)
    
    print("File read done, elapsed time {}s".format(time.time()-start_time))
    print("Node Size: {}".format(g.G.number_of_nodes()))
    print("Edge Size: {}".format(g.G.number_of_edges()))
    
    plot_degree(g.G, args.figure)
    # matplotlib.use('Agg')
    # start_time = time.time()
    # degree = nx.degree_histogram(g.G) #返回图中所有节点的度分布序列
    # x = range(len(degree)) #生成X轴序列，从1到最大度
    # totalDegree = float(sum(degree))
    # y = [z/totalDegree for z in degree] # 将频次转化为频率，利用列表内涵
    # print("Start plotting!")
    # plt.loglog(x, y, color="blue", linewidth=2) #在双对坐标轴上绘制度分布曲线
    # plt.title("Degree Distribution")
    # plt.xlabel("Degree")
    # plt.ylabel("Frequency")
    # print("Figure done, elapsed time {}s".format(time.time()-start_time))
    # if args.figure:
    #     plt.savefig(args.figure)

    # degrees = g.G.degree()
    # degrees_w = g.G.degree(weight='weight')
    # degreesDict = dict(degrees_w)
    # degreesValue = sorted(set(degreesDict.values()))
    # print(degreesValue[:10])
    # degreesCount = [list(degreesDict.values()).count(x) for x in degreesValue]
    # print(operator.eq(degree, degreesCount))
    # print(len(degree))
    # print(len(degreesCount))

    
