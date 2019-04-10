"""
File reader utilities.
Author: Liu Yang
Date: 2019-4-9
"""

import csv
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


class dictReader(object):
    def __init__(self):
        self.short2long = {}
        self.long2short = {}
        self.exchange = {}
        self.pool = {}
        self.eoaSet = set()
        self.scSet = set()
        self.others = []

    def read_dict(self, file_path):
        """
        Data format:
            long_address, short_hash_address, type('eoa' or 'sc')
        """
        start_time = time.time()
        dict_file = open(file_path, 'r')
        dict_reader = csv.reader(dict_file)
        line_num = 0
        for row in dict_reader:
            line_num += 1
            self.long2short[row[0]] = row[1]            
            self.short2long[row[1]] = row[0]
            if row[2] == 'eoa':
                self.eoaSet.add(row[1])
            elif row[2] == 'sc':
                self.scSet.add(row[1])
            else:
                self.others.append(row[0])
        dict_file.close()
        print("{} lines read done, elapsed time {}".format(line_num, time.time()-start_time))


    def read_label(self, file_path, tag):
        """
        Input format:
            tag = {'exchange', 'pool'}
        Data format:
            long_address, notes
        """
        start_time = time.time()
        if tag == 'exchange':
            label = self.exchange
        elif tag == 'pool':
            label = self.pool
        else:
            label = {}
            print("Another kind of label")
        dict_file = open(file_path, 'r')
        dict_reader = csv.reader(dict_file)
        line_num = 0
        for row in dict_reader:
            line_num += 1
            # addr_id = self.long2short[row[0]]
            label[row[0]] = row[1]                
        dict_file.close()
        print("{} lines {} read done, elapsed time {}".format(line_num, tag, time.time()-start_time))


def parse_args():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            conflict_handler='resolve')
    parser.add_argument('--dict', required=True,
                        help='Input dict file')
    parser.add_argument('--graph_type', default='CIG', choices=['MFG', 'CIG', 'CCG'],
                        help='Input graph type')
    parser.add_argument('--graph_format', default='edgelist', choices=['adjlist', 'edgelist'],
                        help='Input graph format')
    parser.add_argument('--output',
                        help='Output representation file')
    parser.add_argument('--directed', action='store_true',
                        help='Treat graph as directed.')
    parser.add_argument('--exchange', default='',
                        help='The file of exchange accounts')
    parser.add_argument('--pool', default='',
                        help='The file of mining pool accounts')
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



if __name__ == "__main__":
    args = parse_args()
    node_dict = dictReader()
    node_dict.read_dict(args.dict)
    print("EOA Size: {}".format(len(node_dict.eoaSet)))
    print("SC Size: {}".format(len(node_dict.scSet)))
    print("Account Size: {}".format(len(node_dict.long2short.keys()))) 
    if args.exchange:
        node_dict.read_label(args.exchange, 'exchange')
    if args.pool:
        node_dict.read_label(args.pool, 'pool')