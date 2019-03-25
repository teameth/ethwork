# from GetGethBlockchain import GetGethBlockchain
from GetGethSC import GetGethBlockchain


def generateBlockchain(start_number,
					   end_number,
					   host='http://localhost', 
					   port=8601
					   ):
	g = GetGethBlockchain(port, host)
	g.storeBlocksToCsv(start_number, end_number)
	# g.storeBlocksFromDict(start_number, end_number)	


if __name__ == '__main__':
	generateBlockchain(6703000,6703001)
