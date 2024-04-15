import networkx as nx


def centrality_betweenness(roads_graph):
    cb = nx.betweenness_centrality(G=roads_graph)
    return sorted(cb.items(), key=lambda x: x[1], reverse=True)


def random_walk_betweenness(roads_graph):
    rwb = nx.current_flow_betweenness_centrality(G=roads_graph.to_undirected())
    return sorted(rwb.items(), key=lambda x: x[1], reverse=True)


def page_rank(roads_graph):
    pr = nx.pagerank(G=roads_graph)
    return sorted(pr.items(), key=lambda x: x[1], reverse=True)



