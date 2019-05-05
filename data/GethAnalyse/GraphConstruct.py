"""
Construct Transaction Graph.
Author: Liu Yang
Date: 2019-4-10
"""

import networkx as nx
import csv
import os
import re
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('--input', required=True,
                        help='Input data file or dir')
    parser.add_argument('--input_type', default='FILE', choices=['FILE', 'DIR'],
                        help='Input path is a directory or file')
    parser.add_argument('--graph_type', default='CIG', choices=['MFG', 'CIG', 'CCG'],
                        help='Input graph type')
    parser.add_argument('--output',
                        help='Output representation file')
    parser.add_argument('--start', default='',
                        help='Start block id, include in the results')
    parser.add_argument('--end', default='',
                        help='End block id, excluded in the results')
    args = parser.parse_args()
    return args


def add_to_graph(file_path, graph, graph_type, start_block, end_block):
    """
    Data Format:
        Transaction ID, Block ID, Timestamp, Transaction Hash, fromAddress, toAddress, Value
    """
    start_time = time.time()
    data_file = open(file_path, 'r')
    data_reader = csv.reader(data_file)
    for row in data_reader:
        if int(row[1]) in range(start_block, end_block):
            fromaddr = row[4]
            toaddr = row[5]
            if graph_type == 'CIG':
                value = 1.0
            else:
                value = float(row[6])
            if G.has_edge(fromaddr, toaddr):
                G[fromaddr][toaddr]['weight'] += value
            else:
                G.add_edge(fromaddr, toaddr, weight=value)
    data_file.close()
    print("file {} read done, elapsed time {}".format(file_path.split('/')[-1], time.time()-start_time))



if __name__ == "__main__":
    args = parse_args()
    start_time = time.time()
    G = nx.DiGraph()
    start_id = int(args.start)
    end_id = int(args.end)
    if args.input_type == 'DIR':
        file_lst = os.listdir(args.input)
        for filename in file_lst:
            if filename.find(args.graph_type) != -1: # Graph type filtering
                id_str = re.findall("\d+", filename)  # the filename is supposed to contain two integers
                id_int = list(map(int, id_str))
                if len(id_int) != 2:
                    print("Filename {} does not contain two integers".format(filename))
                if min(id_int)>=end_id or max(id_int)<=start_id:
                    print(filename+' skipped!')
                    continue
                add_to_graph(args.input + filename, G, args.graph_type, start_id, end_id)
    else:
        add_to_graph(args.input, G, args.graph_type, start_id, end_id)
    
    print("Graph construction done, elapsed time {}s".format(time.time()-start_time))
    print("Node Size: {}".format(G.number_of_nodes()))
    print("Edge Size: {}".format(G.number_of_edges()))

    G_int = nx.relabel.convert_node_labels_to_integers(G, first_label=0, ordering="default", label_attribute='address')
    # addressDict = nx.get_node_attributes(G_int, 'address')
    # print(addressDict.items())
    nx.write_edgelist(G_int, args.output, delimiter=' ', data=False)
    
    # nx.write_weighted_edgelist(G, args.output, delimiter='\t')
