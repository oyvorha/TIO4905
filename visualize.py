import matplotlib.pyplot as plt
import networkx as nx


def draw_routes(dict_routes, stations):
    g = nx.DiGraph()
    colors = ['red', 'blue']
    color_index = 0
    for route in dict_routes.values():
        g.add_edges_from(route, color=colors[color_index])
        color_index += 1
    
    nx.nx_pydot.write_dot(g, 'DiGraph.dot')
    pos = nx.drawing.nx_agraph.graphviz_layout(g, prog='dot')
    nx.draw(g, pos, with_labels=True)
    plt.show()
