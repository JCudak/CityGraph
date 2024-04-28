import matplotlib.colors as mcolors
import matplotlib.cm as cm
import osmnx as ox
import math
import folium
import simple


def retrieve_road_graph(place_name: str, custom_filter: str):
    road_graph = ox.graph_from_place(place_name, custom_filter=custom_filter, simplify=False)
    road_graph = simple.simplify_graph(road_graph)
    return ox.graph_to_gdfs(road_graph, nodes=True, edges=True)

def retrieve_graph(gdf_nodes, gdf_edges):
    return ox.graph_from_gdfs(gdf_nodes, gdf_edges)


def color_nodes(c_measures):
    c_measures = dict(c_measures)
    c_measures = {node_id: math.log(betweenness_value + 1)  # 1 to avoid log(0)
                      for node_id, betweenness_value in c_measures.items()}

    colors = [(0, 1, 0), (1, 1, 0), (1, 0, 0)]  # GREEN, YELLOW, RED
    cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)

    min_betweenness = min(c_measures.values())
    max_betweenness = max(c_measures.values())

    norm = mcolors.Normalize(vmin=min_betweenness, vmax=max_betweenness)
    cmap_scaled = cm.ScalarMappable(norm=norm, cmap=cmap)

    node_colors = {node_id: mcolors.to_hex(cmap_scaled.to_rgba(betweenness_value))
                   for node_id, betweenness_value in c_measures.items()}

    # sns.heatmap(np.random.rand(5, 5), cmap=cmap)
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')
    # plt.show()

    return node_colors


def create_map(nodes, edges, node_colors=None):
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

    for node_id, row in nodes.iterrows():
        with open('popups/popup_style.css', 'r') as f:
            css = f.read()
        with open('popups/node_popup.html', 'r') as f:
            html_template = f.read()

        html_content = html_template.replace('{{node_id}}', str(node_id))
        iframe_html = f"<style>{css}</style>{html_content}"

        iframe = folium.IFrame(html=iframe_html, width=180, height=100)

        folium.CircleMarker(
            location=(row['y'], row['x']),
            radius=2,
            color='red' if node_colors is None else node_colors[node_id],
            fill=True,
            tooltip=folium.Tooltip(f'Node ID: {node_id}'),
            popup=folium.Popup(iframe, parse_html=True)
        ).add_to(folium_map)

    folium_map.save('map.html')
