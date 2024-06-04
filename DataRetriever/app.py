import webbrowser
from centralities import random_walk_betweenness, centrality_betweenness, page_rank, local_clustering_coefficient, eigenvector, closeness
from utils import color_nodes, color_edges, create_map, retrieve_road_graph
from difference_graph import retrieve_difference_graph
from copy import deepcopy

initial_place = "Krakow, Lesser Poland, Poland"
filter_string = ('["highway"~"motorway|trunk|primary|secondary|tertiary|road|residential|motorway_link|trunk_link|'
                 'primary_link|secondary_link|tertiary|link|living_street|unclassified"]["access"!="no"]')

old_graph = retrieve_road_graph(initial_place, filter_string)
road_graph = deepcopy(old_graph) 
road_graph_sum = deepcopy(old_graph)

added_edges = []
deleted_edges = []
old_graph_centralities = ()

centralities = {
    'Random Walk Betweenness': random_walk_betweenness(road_graph),
    'Centrality Betweenness': centrality_betweenness(road_graph),
    'Page Rank': page_rank(road_graph),
    'Local Clustering Coefficient': local_clustering_coefficient(road_graph),
    'Closeness Centrality': closeness(road_graph),
    'Eigenvector Centrality': eigenvector(road_graph)
}

current_centrality = 'Centrality Betweenness'


def get_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a correct number!")


def parse_edge_id_input():
    edge_id_str = input("Enter edge id in format (node1, node2, key): ")
    try:
        node1, node2, key = map(int, edge_id_str.strip("() ").split(","))
        return (node1, node2, key)
    except ValueError:
        print("Invalid input format. Please use the format (node1, node2, key).")
        return None


def handle_centrality_method_switch():
    print("1 - Random Walk Betweenness\n"
          "2 - Centrality Betweenness\n"
          "3 - Page Rank\n"
          "4 - Local Clustering Coefficient\n"
          "5 - Eigenvector Centrality\n"
          "6 - Closeness Centrality\n"
          "5 - Back")
    choice = get_number("Choose a centrality measure: ")
    centrality_options = {
        1: 'Random Walk Betweenness',
        2: 'Centrality Betweenness',
        3: 'Page Rank',
        4: 'Local Clustering Coefficient',
        5: 'Eigenvector Centrality',
        6: 'Closeness Centrality'
    }
    selected = centrality_options.get(choice)
    if selected:
        global current_centrality
        current_centrality = selected
        print(f"{selected} has been selected as the current centrality.")


def add_edge(road_graph):
    edge_id = parse_edge_id_input()
    if edge_id:
        weight = float(input("Enter weight for the edge: "))
        road_graph.add_edge(*edge_id, weight=weight)
        road_graph_sum.add_edge(*edge_id, weight=weight)
        added_edges.append(edge_id)
        print(f"Edge {edge_id} added with weight {weight}.")


def delete_edge(road_graph):
    edge_id = parse_edge_id_input()
    if edge_id and road_graph.has_edge(*edge_id):
        road_graph.remove_edge(*edge_id)
        deleted_edges.append(edge_id)
        print(f"Edge {edge_id} removed.")
    else:
        print("Edge does not exist.")


def display_graph(road_graph):
    global old_graph_centralities
    computed_centralities = centralities[current_centrality]

    if old_graph_centralities == () or old_graph_centralities[0] != current_centrality: 
        old_graph_centralities = (current_centrality, computed_centralities)

    node_colors = color_nodes(centralities[current_centrality])
    create_map(road_graph, node_colors)
    webbrowser.open('map.html')


def read_graph_data(custom_filter):
    place_name = input("Enter place name: ")
    new_road_graph = retrieve_road_graph(place_name, custom_filter)

    if new_road_graph:
        global old_graph, road_graph, road_graph_sum, added_edges, deleted_edges, old_graph_centralities
        old_graph = deepcopy(road_graph)
        road_graph = new_road_graph
        road_graph_sum = deepcopy(new_road_graph)
        added_edges = []
        deleted_edges = []
        old_graph_centralities = ()

        global centralities
        centralities = {
            'Random Walk Betweenness': random_walk_betweenness(road_graph),
            'Centrality Betweenness': centrality_betweenness(road_graph),
            'Page Rank': page_rank(road_graph),
            'Local Clustering Coefficient': local_clustering_coefficient(road_graph),
            'Closeness Centrality': closeness(road_graph),
            'Eigenvector Centrality': eigenvector(road_graph)
        }
        print("Graph data has been updated and centralities recalculated.")


def generate_difference(old_graph, curr_graph):
    diff_measures = retrieve_difference_graph(old_graph, curr_graph, current_centrality, old_graph_centralities[1])
    node_colors = color_nodes(diff_measures)
    edge_colors = color_edges(road_graph_sum.edges, added_edges, deleted_edges)
    create_map(road_graph_sum, node_colors, edge_colors)
    webbrowser.open('diff_map.html')
    print('Difference graph has been generated')



def gui():
    options = {
        1: lambda: display_graph(road_graph),
        2: lambda: add_edge(road_graph),
        3: lambda: delete_edge(road_graph),
        4: handle_centrality_method_switch,
        5: lambda: read_graph_data(filter_string),
        7: lambda: generate_difference(old_graph, road_graph)
    }

    while True:
        print("Choose an option:\n"
              "1 - Display Graph\n"
              "2 - Add Edge\n"
              "3 - Delete Edge\n"
              "4 - Switch Centrality\n"
              "5 - Read New Graph Data\n"
              "6 - Save Graph Data\n"
              "7 - Generate Difference\n"
              "8 - Exit")
        choice = get_number("Enter a number: ")
        if choice == 8:
            break
        option_function = options.get(choice)
        if option_function:
            option_function()


if __name__ == "__main__":
    gui()
