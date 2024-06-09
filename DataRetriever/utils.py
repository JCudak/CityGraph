import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import osmnx as ox
from folium import IFrame, PolyLine, CircleMarker, Popup, Tooltip, Map
import simple
import math


def retrieve_road_graph(place_name: str, custom_filter: str):
    road_graph = ox.graph_from_place(place_name, custom_filter=custom_filter, simplify=False)
    road_graph = simple.simplify_graph(road_graph)
    road_graph = assign_road_weights(road_graph)
    return road_graph


def color_nodes_by_difference(c_measures):
    c_measures = dict(c_measures)
    
    colors = [(1, 1, 0), (1, 0, 0)]  # GREEN, YELLOW, RED
    
    min_betweenness = min(c_measures.values())
    max_betweenness = max(c_measures.values())

    norm = mcolors.Normalize(vmin=min_betweenness, vmax =max_betweenness)

    if min_betweenness < 0:
        colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # GREEN, YELLOW, RED
        norm = mcolors.TwoSlopeNorm(vmin=min_betweenness, vcenter=0, vmax=max(max_betweenness, 0.00001))

    cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)
    cmap_scaled = cm.ScalarMappable(norm=norm, cmap=cmap)

    node_colors = {node_id: mcolors.to_hex(cmap_scaled.to_rgba(betweenness_value))
                   for node_id, betweenness_value in c_measures.items()}
    return node_colors


def color_nodes(c_measures):
    c_measures = dict(c_measures)
    c_measures = {node_id: math.log(betweenness_value + 100)  # to avoid log(0)
                  for node_id, betweenness_value in c_measures.items()}
    
    values = np.array(list(c_measures.values()))
    avg = np.mean(values)
    std = np.std(values)
    
    lower_bound = avg - std
    upper_bound = avg + std
    clamped_values = {node_id: min(max(betweenness_value, lower_bound), upper_bound)
                      for node_id, betweenness_value in c_measures.items()}

    colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # GREEN, YELLOW, RED
    cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)

    min_betweenness = min(clamped_values.values())
    max_betweenness = max(clamped_values.values())

    norm = mcolors.Normalize(vmin=min_betweenness, vmax=max_betweenness)
    cmap_scaled = cm.ScalarMappable(norm=norm, cmap=cmap)

    node_colors = {node_id: mcolors.to_hex(cmap_scaled.to_rgba(betweenness_value))
                   for node_id, betweenness_value in clamped_values.items()}

    return node_colors


def color_edges(total_e, added_e, deleted_e):
    colored_edges = {}

    for edge in total_e:
        if edge in added_e:
            colored_edges[edge] = 'green'
        elif edge in deleted_e:
            colored_edges[edge] = 'red'
        else:
            colored_edges[edge] = 'blue'
    return colored_edges


def create_map(road_graph, node_colors=None, edge_colors=None, centrality_measures=None, difference_measures=None):
    nodes, edges = ox.graph_to_gdfs(road_graph, nodes=True, edges=True)
    folium_map = Map(location=[nodes['y'].mean(), nodes['x'].mean()], zoom_start=15, tiles='cartodbpositron')

    with open('popups/popup_style.css', 'r') as f:
        css = f.read()
    with open('popups/popup.html', 'r') as f:
        html_template = f.read()
    with open('popups/copy_to_clipboard.js', 'r') as f:
        js = f.read()

    def create_popup(item_id, item_type, height=100, centrality_measure=None, difference_measure=None):
        popup_content = html_template.replace('{{item_info}}', f"{item_id}")
        popup_content = popup_content.replace('{{info_name}}', f"{item_type} ID")

        if centrality_measure is not None:
            popup_content += f"<p>Centrality Value: {centrality_measure}</p>"

        if difference_measure is not None:
            popup_content += f"<p>Difference Value: {difference_measure}</p>"

        iframe_html = f"<style>{css}</style><script>{js}</script>{popup_content}"
        return Popup(IFrame(html=iframe_html, width=180, height=height), parse_html=True)

    # Add edges to the map
    for edge_id, row in edges.iterrows():
        road_type = row['highway']
        points = [(y, x) for x, y in zip(row['geometry'].xy[0], row['geometry'].xy[1])]
        PolyLine(
            locations=points,
            color='blue' if edge_colors is None else edge_colors[edge_id],
            weight=2,
            arrow_length=4,
            arrow_head=2,
            road_type=road_type,
            tooltip=Tooltip(f'Edge ID: {edge_id}, Road type: {road_type}'),
            popup=create_popup(edge_id, 'Edge', height=120)
        ).add_to(folium_map)

    # Add nodes to the map
    for node_id, row in nodes.iterrows():
        color = 'red' if node_colors is None else node_colors[node_id]
        CircleMarker(
            location=(row['y'], row['x']),
            radius=2,
            color=color,
            fill=True,
            tooltip=Tooltip(f'Node ID: {node_id}'),
            popup=create_popup(
                    node_id, 
                    'Node', 
                    road_graph,
                    centrality_measure=centrality_measures[node_id] if centrality_measures is not None else None,
                    difference_measure=difference_measures[node_id] if difference_measures is not None else None
            )
        ).add_to(folium_map)

    folium_map.save('map.html') if edge_colors is None else folium_map.save('diff_map.html')


def assign_road_weights(road_graph):
    road_type_weights = {
        'motorway': 0.1,
        'motorway_link': 0.1,
        'trunk': 0.3,
        'trunk_link': 0.3,
        'primary': 0.5,
        'primary_link': 0.5,
        'secondary': 0.6,
        'secondary_link': 0.6,
        'tertiary': 0.7,
        'tertiary_link': 0.7,
        'residential': 0.8,
        'service': 0.8,
        'track': 0.8
    }

    for u, v, data in road_graph.edges(keys=False, data=True):
        road_type = data.get('highway')
        if isinstance(road_type, list):
            first_highway = road_type[0]
        else:
            first_highway = road_type
        data['weight'] = road_type_weights.get(first_highway, 0.9)
    return road_graph
