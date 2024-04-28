import webbrowser

from DataRetriever.utils import retrieve_road_graph
from gui import gui

if __name__ == '__main__':
    place_name = "Kurdwanów, Podgórze, Krakow, Lesser Poland, Poland"
    custom_filter = ('["highway"~"motorway|trunk|primary|secondary|tertiary|road|residential|motorway_link|trunk_link|'
                     'primary_link|secondary_link|tertiary|link|living_street|unclassified|service"]["access"!="no"]')
    nodes, edges = retrieve_road_graph(place_name, custom_filter)

    gui(nodes, edges)