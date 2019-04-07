''' 
A multiprocessing scripts to get code from local eth server
'''

import csv
import binascii
import requests
import json
from multiprocessing import Pool
import sys
import time
from web3 import Web3


        
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
    
 

if __name__ == '__main__':
    node_dict = '/home/liuy/Documents/qinz/dict' if len(sys.argv) <= 1 else sys.argv[1]    
    start_time = time.time()
    dict_file = open(node_dict, 'r')
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
    
    start_time = time.time()
    pool = Pool(20)  
    nodeTypeList = pool.map(getType, addrTupleList)  
    pool.close()
    pool.join()
    # nodeTypeList = getTypefromList(addrTupleList)
    print("Query done, elapsed time {}s".format(time.time()-start_time))   

    start_time = time.time()
    out_file = open('/home/liuy/Documents/qinz/node_dict', 'w')    
    dict_writer = csv.writer(out_file) 
    for nt in nodeTypeList: 
        dict_writer.writerow(list(nt))
    out_file.close()
    print("{} lines written done, elapsed time {}".format(len(nodeTypeList), time.time()-start_time))
    


	
			
	
			
	