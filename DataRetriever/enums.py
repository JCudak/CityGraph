from enum import Enum


class UserOption(Enum):
    display_graph = 1
    add_edge = 2
    delete_edge = 3
    calculate_centralities = 4
    read_graph_data = 5
    save_graph_data = 6
    generate_difference = 7


class Centrality(Enum):
    random_walk_betweenness = 1
    centrality_betweenness = 2
    page_rank = 3
    local_clustering_coefficient = 4