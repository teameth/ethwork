''' 
A class to interact with node and to save data to csv file
'''

import csv
import binascii
import requests
import json
import sys
import time
from web3 import Web3


class GetNodeType:
    '''
    a class to interact with node and to save data to csv file

    Description:
    ----------------
    Before starting, make sure geth is running in rpc
    eg the config of geth is (geth --rpc --rpcaddr 127.0.0.1 --rpcport 8601) 
    
    Parameters:
    Default behavior:
        getGethBlockchain = GetGethBlockchain()
        
    Get  the data from a particular number
        block = getGethBlockchain.getBlock(block_number)
    Save the blocks to csv file
        getGethBlockchain.storeBlocksToCsv(start_number, end_number)

    '''

    def __init__(self,
                    rpc_port=8601, 
                    host='http://localhost'
    ):

        ''' Initialize the class'''
        print('start the class')
        self.url = '{}:{}'.format(host, rpc_port)
        self.headers = {'content-type': 'application/json'}
        self.wb = Web3(Web3.HTTPProvider(self.url))


    def rpcRequest(self, method, params, key):
        '''make the request to geth rpcport'''
        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            'id': 0
        }
        
        res = requests.post(self.url, 
                        data=json.dumps(payload),
                        headers=self.headers).json()
        return res[key]
        
        
    def getType(self, addr):
        """
            Judge the input address is external owned account or smart contract(eth.getCode).
            Convert the long address into a short hash code.
        """
        if isinstance(addr, str):
            # long_addr = str.encode(addr.strip('0x'))
            # short_addr = '%x'%(binascii.crc32(long_addr)&0xffffffff)
            checksum = self.wb.toChecksumAddress(addr)
            sc_code = self.wb.eth.getCode(checksum)
            flag = 'sc' if len(sc_code) > 2 else 'eoa'
            return flag   
        else:
            return None     
    
 

if __name__ == '__main__':
    node_dict = '/home/liuy/Documents/qinz/dict' if len(sys.argv) <= 1 else sys.argv[1]
    g = GetNodeType()
    line_num = 0
    query_num = 1000
    print_per = 1000000
    start_time = time.time()
    dict_file = open(node_dict, 'r')
    out_file = open('/home/liuy/Documents/qinz/node_type_dict_all', 'w')
    dict_reader = csv.reader(dict_file)
    dict_writer = csv.writer(out_file)
    for row in dict_reader:
        line_num += 1
        addr = row[0]
        short = row[1]
        nodeType = g.getType(addr)
        dict_writer.writerow([addr, short, nodeType])
        if line_num % print_per == 0:
            print("{} lines done, elapsed time {}s".format(line_num, time.time()-start_time))       
            start_time = time.time()
        # if line_num > query_num:
        #     break
    print("{} lines done, elapsed time {}s".format(line_num, time.time()-start_time))       
    dict_file.close()
    out_file.close()
    


	
			
	
			
	