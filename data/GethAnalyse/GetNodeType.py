''' 
A multiprocessing scripts to get code from local eth server
'''

import csv
import binascii
import requests
import json
from multiprocessing import Pool
import networkx as nx
import sys
import time
from web3 import Web3
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('--dir', required=True,
                        help='Input data file dir')
    parser.add_argument('--graph_type', default='CIG', choices=['MFG', 'CIG', 'CCG'],
                        help='Input graph type')
    parser.add_argument('--graph_format', default='edgelist', choices=['adjlist', 'edgelist'],
                        help='Input graph format')
    parser.add_argument('--output',
                        help='Output representation file')
    parser.add_argument('--directed', action='store_true',
                        help='Treat graph as directed.')
    parser.add_argument('--label', default='',
                        help='The file of node label')
    parser.add_argument('--feature_file', default='',
                        help='The file of node features')
    parser.add_argument('--weighted', action='store_true',
                        help='Treat graph as weighted')
    args = parser.parse_args()
    return args

        
def getType(addrTuple):
    """
        Judge the input address is external owned account or smart contract(eth.getCode).
        Convert the long address into a short hash code.
    """
    wb = Web3(Web3.HTTPProvider('http://localhost:8601'))
    if isinstance(addrTuple[0], str):
        checksum = wb.toChecksumAddress(addrTuple[0])
        sc_code = wb.eth.getCode(checksum)
        flag = 'sc' if len(sc_code) > 2 else 'eoa' 
    else:
        flag = None   
    return (addrTuple[0], addrTuple[1], flag)  


def getTypefromList(addrTupleList):
    wb = Web3(Web3.HTTPProvider('http://localhost:8601'))
    results = []
    for addrTuple in addrTupleList:
        if isinstance(addrTuple[0], str):
            checksum = wb.toChecksumAddress(addrTuple[0])
            sc_code = wb.eth.getCode(checksum)
            flag = 'sc' if len(sc_code) > 2 else 'eoa'
            results.append((addrTuple[0], addrTuple[1], flag))
    return results


def read_dict(file_path):
    start_time = time.time()
    dict_file = open(file_path, 'r')
    dict_reader = csv.reader(dict_file)
    line_num = 0
    query_num = 10000
    addrTupleList = []
    for row in dict_reader:
        line_num += 1
        addrTupleList.append(tuple(row))
        # if line_num >= query_num:
        #     break
    dict_file.close()
    print("{} lines read done, elapsed time {}".format(len(addrTupleList), time.time()-start_time))
    return addrTupleList


def getTypeParellel(addrTupleList, pool_num=10):
    start_time = time.time()
    pool = Pool(pool_num)  
    nodeTypeList = pool.map(getType, addrTupleList)  
    pool.close()
    pool.join()
    print("Query done, elapsed time {}s".format(time.time()-start_time)) 
    return nodeTypeList


def write_dict(out_path, nodeTypeList):
    start_time = time.time()
    out_file = open(out_path, 'a')    
    dict_writer = csv.writer(out_file) 
    for nt in nodeTypeList: 
        dict_writer.writerow(list(nt))
    out_file.close()
    print("{} lines written done, elapsed time {}".format(len(nodeTypeList), time.time()-start_time))


def generate_dict_from_graph(graph_file):
    G = nx.read_weighted_edgelist(graph_file, delimiter='\t', create_using=nx.DiGraph)
    node_lst = G.nodes
    
    


if __name__ == '__main__':
    node_dict = './data/node_dict/part_' if len(sys.argv) <= 1 else sys.argv[1]    
    for i in ['07', '08', '09', '10', '11', '12']:
        addrTupleList = read_dict(node_dict+i)
        # nodeTypeList = getTypefromList(addrTupleList)
        nodeTypeList = getTypeParellel(addrTupleList)
        write_dict('./data/node_dict/node_type_dict', nodeTypeList)

	
			
	
			
	