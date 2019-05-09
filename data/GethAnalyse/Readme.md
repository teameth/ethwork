## Server 
cloud77:/home/liuy/Documents/BlockChain/GetGeth-Liu/

## GraphConstruct.py
- python readgraphfromfile.py --input ../OpenNE/data/ethereum/CIGMFG --graph_type MFG --directed --weighted --label ../evaluate/data/labellist-22.csv
- python readgraphfromfile.py --input ../OpenNE/data/ethereum/CIG --graph_type CIG --directed --weighted --label ../evaluate/data/labellist-22.csv

- python GraphConstruct.py --dir ./data/ --graph_type CIG --output ./data/trans_graph/CIG-long-650


## TemporalGraph.py
Construct temporal graph from certain blocks
usage: TemporalGraph.py [-h] --input INPUT [--input_type {FILE,DIR}]
                        [--graph_type {MFG,CIG,CCG}] [--output OUTPUT]
                        [--start START] [--end END]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT         Input data file or dir (default: None)
  --input_type {FILE,DIR}
                        Input path is a directory or file (default: FILE)
  --graph_type {MFG,CIG,CCG}
                        Input graph type (default: CIG)
  --output OUTPUT       Output representation file (default: None)
  --start START         Start block id, include in the results (default: )
  --end END             End block id, excluded in the results (default: )

Command lines:
- python TemporalGraph.py --input ./data/MFG-Block6000000To6500000.csv --graph_type MFG --start 6000000 --end 6100000 --output ./data/trans_graph/MFG-10w
- python TemporalGraph.py --input ./data/ --input_type DIR --graph_type MFG --start 5000000 --end 5500000 --output ./data/trans_graph/MFG-500w+50w

