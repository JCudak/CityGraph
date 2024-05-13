from utils import color_nodes, create_map
from centralities import random_walk_betweenness
from centralities import centrality_betweenness
from centralities import page_rank
from centralities import local_clustering_coefficient
from centralities import eigenvector
from centralities import closeness


def _compute_centralities(type, old_graph, new_graph, old_measure):
    old_graph_measure = [tuple()] if old_measure is None else old_measure
    new_graph_measure = [tuple()]

    match type:
        case 'Random Walk Betweenness':
            if old_measure is None:
                old_graph_measure = random_walk_betweenness(old_graph) 
            new_graph_measure = random_walk_betweenness(new_graph)

        case 'Centrality Betweenness':
            if old_measure is None:
                old_graph_measure = centrality_betweenness(old_graph)
            new_graph_measure = centrality_betweenness(new_graph)

        case 'Page Rank':
            if old_measure is None:
                old_graph_measure = page_rank(old_graph)
            new_graph_measure = page_rank(new_graph)

        case 'Local Clustering Coefficient':
            if old_measure is None:
                old_graph_measure = local_clustering_coefficient(old_graph)
            new_graph_measure = local_clustering_coefficient(new_graph)

        case 'Eigenvector Centrality':
            if old_measure is None:
                old_graph_measure = eigenvector(old_graph)
            new_graph_measure = eigenvector(new_graph)

        case 'Closeness Centrality':
            if old_measure is None:
                old_graph_measure = closeness(old_graph)
            new_graph_measure = closeness(new_graph)

        case _:
            print('Operation is not supporeted')

    return old_graph_measure, new_graph_measure


def _compute_difference(old_measure, new_measure):
    old_measure = dict(old_measure)
    new_measure = dict(new_measure)

    diff_measure = {}

    for id, _ in old_measure.items():
        diff_measure[id] = new_measure[id] - old_measure[id]

    return list(diff_measure.items())

def retrieve_difference_graph(old_graph, new_graph, measure_method, old_measure = None):
    old_measure, new_measure = _compute_centralities(measure_method, old_graph, new_graph, old_measure)
    diff_measure = _compute_difference(old_measure, new_measure)
    return diff_measure
