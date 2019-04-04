''' 
A class to interact with node and to save data to csv file
'''


import GetGethBlockchainUtility
import csv
import binascii
import requests
import json
import time
from datetime import datetime
from web3 import Web3


class GetGethBlockchain:
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
        
    def getOneBlock(self, n):
        '''
            get one block data
            param: n the number of the block
        '''
        data = self.rpcRequest('eth_getBlockByNumber', [hex(n), True], 'result')
        block = GetGethBlockchainUtility.decodeBlock(data)
        return block

    def printOneBlock(self, block):
        '''
            Print the transactions in one block
        '''
        count = 0
        time = datetime.fromtimestamp(block['timestamp']).isoformat()
        for t in block['transactions']:
            count += 1
            print("Creating time: {}".format(time))
            print("Transaction hash: {}".format(t['transactionhash']))
            print("From: {}".format(t['from']))
            print("To: {}".format(t['to']))
            print("ETH: {}".format(t['value']))

    
    def shortHash(self, addr):
        """
            Judge the input address is external owned account or smart contract(eth.getCode).
            Convert the long address into a short hash code.
        """
        if isinstance(addr, str):
            long_addr = str.encode(addr.strip('0x'))
            short_addr = '%x'%(binascii.crc32(long_addr)&0xffffffff)
            checksum = self.wb.toChecksumAddress(addr)
            sc_code = self.wb.eth.getCode(checksum)
            if len(sc_code) > 2:
                flag = 'sc'
            else:
                flag = 'eoa'
            return short_addr, flag   
        else:
            return None, None     
    

    def storeBlocksToCsv(self, start_number, end_number):
        '''
            store the block between start_number to end_number to csv file
            Output Format:
                Transaction ID, Block ID, Timestamp, Transaction Hash, From, From(Short Hash), FromType, To, To(ShortHash), ToType, Value
        '''
        print("starting storing.......")
        trans_id = 0
        MFG_csv_file = open('./data/MFG-Block{}To{}.csv'.format(start_number, end_number), 'w')
        CIG_csv_file = open('./data/CIG-Block{}To{}.csv'.format(start_number, end_number), 'w')   
        CCG_csv_file = open('./data/CCG-Block{}To{}.csv'.format(start_number, end_number), 'w')                     
        MFGwriter = csv.writer(MFG_csv_file)
        CIGwriter = csv.writer(CIG_csv_file)
        CCGwriter = csv.writer(CCG_csv_file)
        start_time = time.time()                        
        for i in range(start_number, end_number):
            if (i-start_number)%10000 == 0:
                print('Block {} completed, elapsed time {}s!'.format(i, time.time()-start_time))			
                print('complete %d %%...' % (100*(i-start_number)/(end_number-start_number)))
                start_time = time.time()
            block = self.getOneBlock(i)
            for t in block['transactions']:
                trans_id += 1
                # f_short, f_type = self.shortHash(t['from'])
                # t_short, t_type = self.shortHash(t['to'])
                # o_list = [str(trans_id), block['height'], block['timestamp'], t['transactionhash'], 
                #                         t['from'], f_short, f_type, t['to'], t_short, t_type, t['value']]
                o_list = [str(trans_id), block['height'], block['timestamp'], t['transactionhash'], t['from'], t['to'], t['value']]
                if t['to'] is None:
                    CCGwriter.writerow(o_list)
                    continue
                if len(t['input']) > 2:
                    CIGwriter.writerow(o_list)
                if t['value'] > 1e-20:
                    MFGwriter.writerow(o_list)
        MFG_csv_file.close()
        CIG_csv_file.close()
        CCG_csv_file.close()        
        print('{} transactions completed!'.format(trans_id))


	
			
	
			
	