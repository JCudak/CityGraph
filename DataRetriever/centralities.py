import networkx as nx


def betweenness(roads_graph):
    b=nx.betweenness_centrality(G=roads_graph)
    max_value = max(b.values())
    max_key = [key for key, value in b.items() if value == max_value][0]
    print(max_key, max_value)

