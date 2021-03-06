#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import numpy as np
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter



class QuantitativeEvaluator:
    """
    Analyse the embedding results.
        :nt2vecs is a dict whose key is the node address and value is the embedding vector
        :nt2type is a dict whose key is the node address and value is the node type, 'Sc' or 'No'
        :query_neighbor is a dict whose key is the node address and value is a neighbor address list
        :query_neighbor_dist is a dict whose key is the node address and value is a 2-tuple list,
                                        the 2-tuple is like (address, distance)        
    """
    def __init__(self, embed_file, label_file, node_file):
        self.nt2vecs = dict()
        self.nt2type = dict()
        self.label_account = []
        self.query_neighbor = dict()
        self.query_neighbor_dist = dict()          
        self.read_embedding(embed_file)
        self.read_label(label_file)
        self.read_node_type(node_file)
        self.get_neighbors(self.label_account, self.get_certain_nodes('No'))


    def read_embedding(self, file_path):
        fr = open(file_path, 'r')
        for line in fr.readlines():
            lineArr = line.strip().split()
            line_node = lineArr[0]
            lineArr.pop(0)
            line_vec = np.array([float(i) for i in lineArr])
            self.nt2vecs[line_node] = line_vec
        fr.close()
        print("{} embedding vectors read done!".format(len(self.nt2vecs)))


    def read_label(self, file_path):
        with open(file_path, 'r') as labelfile:
            exchange_account = csv.reader(labelfile)
            for notes, address in exchange_account:
                self.label_account.append(address)
        print("{} labeled nodes read done!".format(len(self.label_account)))
        

    def read_node_type(self, file_path):
        fr = open(file_path, 'r')
        for line in fr.readlines():
            node_long, node_short, nt = line.strip().split(',')
            self.nt2type[node_short] = nt
        fr.close()
        print('{} nodes type read done!'.format(len(self.nt2type)))


    def get_certain_nodes(self, nt):
        nodeList = []
        for node in self.nt2vecs.keys():
            if self.nt2type[node] == nt:
                nodeList.append(node)
        return nodeList


    def get_neighbors(self, queries, candidates):
        start_time = time.time()
        for query in queries:
            query_vec = self.nt2vecs[query]
            nbList = []
            for node in candidates:
                node_vec = self.nt2vecs[node]
                dist = np.linalg.norm(query_vec - node_vec)
                if dist < 20:
                    nbList.append((node, dist))
            nbSort = sorted(nbList, key=lambda x: x[1])
            self.query_neighbor[query] = [tup[0] for tup in nbSort]
            self.query_neighbor_dist[query] = nbSort
        print('Neighbors found for {} queries, elapsed time {}s'.format(len(queries), time.time()-start_time))


    def get_metrics(self, k=10):
        p_k = []
        r_k = []
        label = set(self.label_account)
        for query in self.query_neighbor.keys():
            nb = self.query_neighbor[query]
            if len(nb) > k:
                nb = nb[:k]
            interSet = set(nb) & label
            p_k.append(len(interSet)/len(nb))
            r_k.append(len(interSet)/len(label))
        precision = sum(p_k)/len(p_k)
        recall = sum(r_k)/len(r_k)
        print("Precision@{}={}".format(k, precision))
        print("Recall@{}={}".format(k, recall))  
            

    def write_neighbors(self, out_path, k=10):
        fw = open(out_path, 'w')
        for query in self.query_neighbor.keys():
            nb = self.query_neighbor[query]
            if len(nb) > k:
                nb = nb[:k]
            line = '\t'.join([str(p) for p in nb])
            fw.write(query + '\t' + line + '\n')
        fw.close()


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('--embedding', required=True,
                        help='Embedding file')
    parser.add_argument('--label', required=True,
                        help='Labeled accounts file')
    parser.add_argument('--node_type', default='',
                        help='Node type file')
    parser.add_argument('--output', default='./top_neighbors',
                        help='The file of node label')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    evaluator = QuantitativeEvaluator(args.embedding, args.label, args.node_type)
    evaluator.write_neighbors(args.output)
    evaluator.get_metrics(10)
    evaluator.get_metrics(20)    
    



