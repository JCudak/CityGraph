import networkx as nx

def random_walk_betweenness(roads_graph):
    rwb = nx.current_flow_betweenness_centrality(G=roads_graph.to_undirected())
    #print(sorted(rwb.items(),  key=lambda item: item[1]))
    return rwb 



