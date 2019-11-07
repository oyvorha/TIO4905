import matplotlib.pyplot as plt
import networkx as nx


def draw_routes(dict_routes, stations):
    g = nx.DiGraph()
    battery_labels = {}
    for s in stations:
        g.add_node(s)
        battery_labels[s] = "N" + str(s)
    color_map = []
    for route in dict_routes.values():
        route_edges = []
        for edge in route:
            g.add_edge(edge[0], edge[1], weight=edge[3])
            route_edges.append((edge[0], edge[1]))
            battery_labels[edge[0]] += (" - " + str(edge[4]))
        color_map.append(route_edges)

    arc_weight = nx.get_edge_attributes(g, 'weight')
    pos = nx.drawing.nx_agraph.graphviz_layout(g, prog='dot')
    nx.draw_networkx_nodes(g, pos, node_size=400, node_color="yellow")
    nx.draw_networkx_edges(g, pos, edge_color=[get_color(color_map, edge) for edge in g.edges()])
    nx.draw_networkx_labels(g, pos, font_color="black", labels=battery_labels)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=arc_weight)
    plt.show()


def get_color(color_map, edge):
    colors = ['black', 'green', 'blue', 'brown', 'yellow']
    for i in range(len(color_map)):
        if edge in color_map[i]:
            return colors[i]
