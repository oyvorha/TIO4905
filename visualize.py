import matplotlib.pyplot as plt
import networkx as nx


def draw_routes(dict_routes, stations, time_hor):
    g = nx.DiGraph()
    battery_labels = {}
    for s in stations:
        g.add_node(s)
        battery_labels[s] = "S" + str(s)
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
    plt.title("Time horizon = "+str(time_hor))
    plt.show()


def get_color(color_map, edge):
    colors = ['black', 'green', 'blue', 'brown', 'yellow']
    for i in range(len(color_map)):
        if edge in color_map[i]:
            return colors[i]


def visualize(m, fixed, image=True):
    route_dict = {}
    for var in m.getVars():
        if var.varName[0] == 'x' and var.x == 1:
            var_1 = var.varName.split("[")[1]
            var_list = var_1.split(",")
            i = int(var_list[0])
            j = int(var_list[1])
            v = int(var_list[2][:-1])
            if i != 0:
                t = float(m.getVarByName("t[{}]".format(i)).x)
            else:
                t = float(m.getVarByName("t_D[{}]".format(v)).x)
            if i in fixed.stations[1:-1]:
                q = int(m.getVarByName("q[{},{}]".format(i, v)).x)
            else:
                q = 0
            dist = fixed.driving_times[i][j]
            arch = [i, j, t, dist, q]
            if v not in route_dict.keys():
                route_dict[v] = [arch]
            else:
                route = route_dict[v]
                for i in range(len(route)):
                    if route[i][-3] > t:
                        route.insert(i, arch)
                        break
                    else:
                        if i == len(route_dict[v]) - 1:
                            route.append(arch)
        print(var.varName, var.x)
    if image:
        draw_routes(route_dict, fixed.stations, fixed.time_horizon)
    print(route_dict)
    print("Obj: ", m.objVal)
