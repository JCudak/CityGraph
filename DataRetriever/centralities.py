import networkx as nx


def centrality_betweenness(roads_graph):
    cb = nx.betweenness_centrality(G=roads_graph, weight='weight')
    return sorted(cb.items(), key=lambda x: x[1], reverse=True)


def random_walk_betweenness(roads_graph):
    rwb = nx.current_flow_betweenness_centrality(G=roads_graph.to_undirected(), weight='weight')
    return sorted(rwb.items(), key=lambda x: x[1], reverse=True)


def page_rank(roads_graph):
    pr = nx.pagerank(G=roads_graph, weight='weight')
    return sorted(pr.items(), key=lambda x: x[1], reverse=True)


def local_clustering_coefficient(roads_graph):
    G2 = nx.DiGraph(roads_graph)
    return nx.clustering(G=G2.to_undirected(), weight='weight')


def eigenvector(roads_graph):
    G2 = nx.DiGraph(roads_graph)
    return nx.eigenvector_centrality_numpy(G=G2, weight='weight')


def closeness(roads_graph):
    return nx.closeness_centrality(G=roads_graph, distance='weight')

