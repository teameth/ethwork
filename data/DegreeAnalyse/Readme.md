Construct a graph using networkx and conduct degree analysis on the graph.

## Naming Scheme
"{}-{}-{}+{}".format(data_type, graph_type, start_block_id, included_id_num)

- data_type: MFG, CIG, CCG
- graph_type: T (Temporal graph) D (Directed) U (Undirected) W(Weighted)


## Usage
- python readgraphfromfile.py --input ../OpenNE/data/ethereum/CIGMFG --graph_type MFG --directed --weighted --label ../evaluate/data/labellist-22.csv
- python readgraphfromfile.py --input ../OpenNE/data/ethereum/CIG --graph_type CIG --directed --weighted --label ../evaluate/data/labellist-22.csv