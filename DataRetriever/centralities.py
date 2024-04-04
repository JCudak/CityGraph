import networkx as nx

def random_walk_betweenness(roads_graph):
    rwb = nx.current_flow_betweenness_centrality(G=roads_graph.to_undirected())
    return sorted(rwb.items(), key=lambda x: x[1], reverse=True)
