import networkx as nx

def centrality_betweenness(roads_graph):
    b=nx.betweenness_centrality(G=roads_graph)
    max_value = max(b.values())
    max_key = [key for key, value in b.items() if value == max_value][0]
    print(max_key, max_value)


def random_walk_betweenness(roads_graph):
    rwb = nx.current_flow_betweenness_centrality(G=roads_graph.to_undirected())
    return sorted(rwb.items(), key=lambda x: x[1], reverse=True)
