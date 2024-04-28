import networkx as nx
from shapely.geometry import LineString
from shapely.geometry import Point


def _is_endpoint(G, node):
    neighbors = set(list(G.predecessors(node)) + list(G.successors(node)))
    n = len(neighbors)
    d = G.degree(node)

    if node in neighbors:
        return True

    if G.out_degree(node) == 0 or G.in_degree(node) == 0:
        return True

    if not ((n == 2) and (d in {2, 4})):
        return True

    return False


def _build_path(G, endpoint, endpoint_successor, endpoints):
    path = [endpoint, endpoint_successor]

    for this_successor in G.successors(endpoint_successor):
        successor = this_successor
        if successor not in path:
            path.append(successor)
            while successor not in endpoints:
                successors = [n for n in G.successors(successor) if n not in path]

                if len(successors) == 1:
                    successor = successors[0]
                    path.append(successor)

                elif len(successors) == 0:
                    if endpoint in G.successors(successor):
                        return path + [endpoint]

                    return path

            return path

    return path


def _get_paths_to_simplify(G):
    endpoints = {n for n in G.nodes if _is_endpoint(G, n)}

    for endpoint in endpoints:
        for successor in G.successors(endpoint):
            if successor not in endpoints:
                yield _build_path(G, endpoint, successor, endpoints)


def _remove_rings(G):
    nodes_in_rings = set()
    for wcc in nx.weakly_connected_components(G):
        if not any(_is_endpoint(G, n) for n in wcc):
            nodes_in_rings.update(wcc)
    G.remove_nodes_from(nodes_in_rings)
    return G


def simplify_graph(graph, remove_self_loops=True):
    attrs_to_sum = {"length", "travel_time"}

    graph = graph.copy()
    all_nodes_to_remove = []
    all_edges_to_add = []

    for path in _get_paths_to_simplify(graph):
        path_attributes = {}
        for u, v in zip(path[:-1], path[1:]):

            edge_data = list(graph.get_edge_data(u, v).values())[0]
            for attr in edge_data:
                if attr in path_attributes:
                    path_attributes[attr].append(edge_data[attr])
                else:
                    path_attributes[attr] = [edge_data[attr]]

        for attr in path_attributes:
            if attr in attrs_to_sum:
                path_attributes[attr] = sum(path_attributes[attr])
            elif len(set(path_attributes[attr])) == 1:
                path_attributes[attr] = path_attributes[attr][0]
            else:
                path_attributes[attr] = list(set(path_attributes[attr]))

        path_attributes["geometry"] = LineString(
            [Point((graph.nodes[node]["x"], graph.nodes[node]["y"])) for node in path]
        )

        all_nodes_to_remove.extend(path[1:-1])
        all_edges_to_add.append(
            {"origin": path[0], "destination": path[-1], "attr_dict": path_attributes}
        )

    for edge in all_edges_to_add:
        graph.add_edge(edge["origin"], edge["destination"], **edge["attr_dict"])

    graph.remove_nodes_from(set(all_nodes_to_remove))

    graph = _remove_rings(graph)

    if remove_self_loops:
        self_loops = list(nx.selfloop_edges(graph))
        graph.remove_edges_from(self_loops)

    return graph
