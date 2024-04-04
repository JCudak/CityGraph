import osmnx as ox
import folium
import webbrowser

from centralities import random_walk_betweenness

def retrieve_road_graph(place_name: str, network_type: str):
    road_graph = ox.graph_from_place(place_name, network_type=network_type, simplify=True)
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
    place_name = "Podgórze Duchackie, Krakow, Lesser Poland, Poland"
    network_type = "drive"  # "all_private", "all", "bike", "drive", "drive_service", "walk"
    nodes, edges = retrieve_road_graph(place_name, network_type)
    roads_graph = retrieve_graph(nodes, edges)

    rwb = random_walk_betweenness(roads_graph)
    print(rwb)

    create_map(nodes, edges)
    webbrowser.open('map.html')
