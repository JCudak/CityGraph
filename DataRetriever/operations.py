from utils import color_nodes, create_map
from centralities import random_walk_betweenness
from centralities import centrality_betweenness 
from centralities import page_rank
from centralities import local_clustering_coefficient

def _compute_centralities(type, old_graph, new_graph):
    old_graph_measure = [tuple()]
    new_graph_measure = [tuple()] 

    match type:
        case 'Random Walk Betweenness':
            old_graph_measure = random_walk_betweenness(old_graph)
            new_graph_measure = random_walk_betweenness(new_graph)

        case 'Centrality Betweenness':
            old_graph_measure = centrality_betweenness(old_graph)
            new_graph_measure = centrality_betweenness(new_graph)

        case 'Page Rank':
            old_graph_measure = page_rank(old_graph)
            new_graph_measure = page_rank(new_graph)

        case 'Local Clustering Coefficient':
            old_graph_measure = local_clustering_coefficient(old_graph)
            new_graph_measure = local_clustering_coefficient(new_graph)
        case _:
            print('Operation is not supporeted')

    return old_graph_measure, new_graph_measure

def _compute_difference(old_measure, new_measure):
    old_measure = dict(old_measure) 
    new_measure = dict(new_measure)

    diff_measure = {}

    for id, measure in old_measure.items():
        diff_measure[id] = new_measure[id] - old_measure[id]

    return list(diff_measure)

def _retrieve_deleted_edges(old_graph, new_graph):
    old_edges = {edge: old_graph[edge[0]][edge[1]] for edge in old_graph.edges}
    new_edges = {edge: new_graph[edge[0]][edge[1]] for edge in new_graph.edges}

    deleted_edges = {}

    for edge, data in old_edges.items():
        if edge not in new_edges:
            deleted_edges[edge] = data

    return deleted_edges

def _retrieve_added_edges(old_graph, new_graph):
    old_edges = {edge: old_graph[edge[0]][edge[1]] for edge in old_graph.edges}
    new_edges = {edge: new_graph[edge[0]][edge[1]] for edge in new_graph.edges}

    added_edges = {}

    for edge, data in new_edges.items():
        if edge not in old_edges:
            added_edges[edge] = data

    return added_edges


def retrieve_difference_graph(old_graph, new_graph, sum_graph, measure_method):
    old_measure, new_measure =  _compute_centralities(measure_method, old_graph, new_graph)
    diff_measure = _compute_difference(old_measure, new_measure)
    deleted_edges = _retrieve_deleted_edges(old_graph, new_graph)
    added_eges = _retrieve_added_edges(old_graph, new_graph)

                        


    
    

    
    





