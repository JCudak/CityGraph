
from DataRetriever.centralities import random_walk_betweenness, centrality_betweenness, page_rank, \
    local_clustering_coefficient
from DataRetriever.enums import Centrality, UserOption


def get_number():
    try:
        number = int(input())
    except ValueError:
        print("Please enter a correct number!")
    return number


def centralities(roads_graph):
    while True:
        print("1 - random walk betweenness\n"
              "2 - centrality betweenness\n"
              "3 - page_rank\n"
              "4 - local_clustering_coefficient\n"
              "5 - back")

        value = get_number()
        if value == Centrality.random_walk_betweenness.value:
            rwb = random_walk_betweenness(roads_graph)
            print("random_walk_betweenness was count")

        elif value == Centrality.centrality_betweenness.value:
            cb = centrality_betweenness(roads_graph)
            print("centrality_betweenness was count")

        elif value == Centrality.page_rank.value:
            pgb = page_rank(roads_graph)
            print("roads_graph was count")

        elif value == Centrality.local_clustering_coefficient.value:
            lcc = local_clustering_coefficient(roads_graph)
            print("local_clustering_coefficient was count")
        else:
            break


def gui(roads_graph):

    while True:
        print("Choose an option:\n"
              "1 - display graph\n"
              "2 - add edge\n"
              "3 - delete edge\n"
              "4 - calculate centralities\n"
              "5 - read graph data\n"
              "6 - save graph data (with centralities)\n"
              "7 - generate difference\n"
              "Enter a number: ")
        number = get_number()

        if number == UserOption.display_graph.value:
            ...
        elif number == UserOption.add_edge.value:
            print("Enter edge number: ")
            value = get_number()

        elif number == UserOption.delete_edge.value:
            print("Enter edge number: ")
            value = get_number()

        elif number == UserOption.calculate_centralities.value:
            centralities(roads_graph)

        elif number == UserOption.read_graph_data.value:
            ...
        elif number == UserOption.save_graph_data.value:
            ...
        elif number == UserOption.generate_difference.value:
            ...

        number = 0
