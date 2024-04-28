import matplotlib.colors as mcolors
import matplotlib.cm as cm
import osmnx as ox
from folium import IFrame, PolyLine, CircleMarker, Popup, Tooltip, Map
import simple


def retrieve_road_graph(place_name: str, custom_filter: str):
    road_graph = ox.graph_from_place(place_name, custom_filter=custom_filter, simplify=False)

    road_graph = simple.simplify_graph(road_graph)

    return ox.graph_to_gdfs(road_graph, nodes=True, edges=True)


def retrieve_graph(gdf_nodes, gdf_edges):
    return ox.graph_from_gdfs(gdf_nodes, gdf_edges)


def color_nodes(c_measures):
    c_measures = dict(c_measures)
    colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # GREEN, YELLOW, RED
    cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)

    max_betweenness = max(c_measures.values())
    norm = mcolors.Normalize(vmin=0, vmax=max_betweenness)
    cmap_scaled = cm.ScalarMappable(norm=norm, cmap=cmap)

    node_colors = {node_id: mcolors.to_hex(cmap_scaled.to_rgba(betweenness_value))
                   for node_id, betweenness_value in c_measures.items()}

    # sns.heatmap(np.random.rand(5, 5), cmap=cmap)
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')
    # plt.show()

    return node_colors


def create_map(nodes, edges, node_colors=None):
    folium_map = Map(location=[nodes['y'].mean(), nodes['x'].mean()], zoom_start=15, tiles='cartodbpositron')

    # Load CSS and HTML templates, and JavaScript
    with open('popups/popup_style.css', 'r') as f:
        css = f.read()
    with open('popups/node_popup.html', 'r') as f:
        html_template = f.read()
    with open('popups/copy_to_clipboard.js', 'r') as f:
        js = f.read()

    def create_popup(item_id, item_type, height=100):
        popup_content = html_template.replace('{{item_info}}', f"{item_id}")
        popup_content = popup_content.replace('{{info_name}}', f"{item_type} ID")
        iframe_html = f"<style>{css}</style><script>{js}</script>{popup_content}"
        return Popup(IFrame(html=iframe_html, width=180, height=height), parse_html=True)

    # Add edges to the map
    for edge_id, row in edges.iterrows():
        points = [(y, x) for x, y in zip(row['geometry'].xy[0], row['geometry'].xy[1])]
        PolyLine(
            locations=points,
            color='blue',
            weight=2,
            arrow_length=4,
            arrow_head=2,
            tooltip=Tooltip(f'Edge ID: {edge_id}'),
            popup=create_popup(edge_id, 'Edge', 120)
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
            popup=create_popup(node_id, 'Node')
        ).add_to(folium_map)

    folium_map.save('map.html')
