import networkx as nx

def random_walk_betweenness(roads_graph):
    return nx.current_flow_betweenness_centrality(G=roads_graph.to_undirected())
