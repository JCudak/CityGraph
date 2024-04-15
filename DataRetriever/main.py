import osmnx as ox
import networkx as nx
import folium
import webbrowser
import simple
from centralities import random_walk_betweenness


def retrieve_road_graph(place_name: str, custom_filter: str):
    road_graph = ox.graph_from_place(place_name, custom_filter=custom_filter, simplify=False)

    road_graph = simple.simplify_graph(road_graph)

    return ox.graph_to_gdfs(road_graph, nodes=True, edges=True)


def retrieve_graph(gdf_nodes, gdf_edges):
    return ox.graph_from_gdfs(gdf_nodes, gdf_edges)


def create_map(nodes, edges):
    folium_map = folium.Map(location=[nodes['y'].mean(), nodes['x'].mean()], zoom_start=15, tiles='cartodbpositron')

    for _, row in edges.iterrows():
        points = [(y, x) for x, y in zip(row['geometry'].xy[0], row['geometry'].xy[1])]
        folium.PolyLine(
            locations=points,
            color='blue',
            weight=2,
            arrow_length=4,
            arrow_head=2
        ).add_to(folium_map)

    for _, row in nodes.iterrows():
        folium.CircleMarker(
            location=(row['y'], row['x']),
            radius=2,
            color='red',
            fill=True
        ).add_to(folium_map)

    folium_map.save('map.html')


if __name__ == '__main__':
    place_name = "Grzegórzki, Krakow, Lesser Poland, Poland"
    custom_filter = '["highway"~"motorway|trunk|primary|secondary|tertiary|road|residential|motorway_link|trunk_link|primary_link|secondary_link|tertiary|link|living_street|unclassified|service"]["access"!="no"]'
    nodes, edges = retrieve_road_graph(place_name, custom_filter)
    roads_graph = retrieve_graph(nodes, edges)

    rwb = random_walk_betweenness(roads_graph)
    print(rwb)

    create_map(nodes, edges)
    webbrowser.open('map.html')

