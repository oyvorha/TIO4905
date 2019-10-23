from gurobipy import *
from fixed_file_variables import *
from dynamic_file_variables import *
from visualize import draw_routes

f = FixedFileVariables()
d = DynamicFileVariables()

try:
    m = Model("Bicycle")

    # ------ SETS -----------------------------------------------------------------------------
    Stations = f.stations
    Vehicles = f.vehicles

    # ------ FIXED PARAMETERS -----------------------------------------------------------------
    time_horizon = f.time_horizon
    vehicle_cap = f.vehicle_cap
    station_cap = f.station_cap
    driving_times = f.driving_times
    parking_time = f.parking_time
    handling_time = f.handling_time
    M = f.M

    # ------- DYNAMIC PARAMETERS --------------------------------------------------------------
    start_stations = d.start_stations
    init_vehicle_load = d.init_vehicle_load
    init_station_load = d.init_station_load
    init_flat_station_load = d.init_flat_station_load
    ideal_state = d.ideal_state
    driving_to_start = d.driving_to_start
    demand = d.demand
    incoming_rate = d.incoming_rate
    incoming_flat_rate = d.incoming_flat_rate

    # ------ VARIABLES -------------------------------------------------------------------------
    x = m.addVars({(i, j, v) for i in Stations
                     for j in Stations for v in Vehicles}, vtype=GRB.BINARY, lb=0, name="x")
    t = m.addVars({i for i in Stations}, vtype=GRB.CONTINUOUS, lb=0, name="t")
    q = m.addVars({(i, v) for i in Stations for v in Vehicles}, vtype=GRB.INTEGER, lb=0, name="q")
    l_B = m.addVars({i for i in Stations}, vtype=GRB.INTEGER, lb=0, name="l_B")
    l_F = m.addVars({i for i in Stations}, vtype=GRB.INTEGER, lb=0, name="l_F")
    l_V = m.addVars({(i, v) for i in Stations for v in Vehicles}, vtype=GRB.INTEGER, lb=0, name="l_V")
    s_I = m.addVars({i for i in Stations}, vtype=GRB.INTEGER, lb=0, name="s_I")
    s_V = m.addVars({v for v in Vehicles}, vtype=GRB.INTEGER, lb=0, name="s_V")
    v_S = m.addVars({i for i in Stations}, vtype=GRB.INTEGER, lb=0, name="v")
    d = m.addVars({i for i in Stations}, vtype=GRB.CONTINUOUS, lb=0, name="d")

    # ------- FEASIBILITY CONSTRAINTS ----------------------------------------------------------
    # Routing constraints
    m.addConstrs(x.sum(start_stations[v], '*', v) == 1 for v in Vehicles)
    m.addConstrs(x.sum('*', Stations[-1], v) == 1 for v in Vehicles)
    for j in Stations[:-1]:
        for v in Vehicles:
            if j != start_stations[v]:
                m.addConstr(x.sum('*', j, v) - x.sum(j, '*', v) == 0)
    m.addConstrs(x.sum('*', j, '*') <= 1 for j in Stations[1:-1])
    for v in Vehicles:
        if start_stations[v] != 0:
            m.addConstr(x.sum('*', start_stations[v], '*') == 0)
    m.addConstrs(x.sum('*', 0, v) <= 1 for v in Vehicles)
    m.addConstrs(x.sum('*', '*', v) <= (len(Stations)-1) for v in Vehicles)

    # Time Constraints
    m.addConstrs(t[i] + parking_time + handling_time * q.sum(i, '*') + driving_times[i][j]
                 - t[j] - time_horizon * (1-x.sum(i, j, '*')) <= 0 for i in Stations for j in Stations[:-1])
    m.addConstrs(t[start_stations[v]] >= driving_to_start[v] for v in Vehicles)
    m.addConstrs(t[i] - time_horizon - M * x.sum(i, Stations[-1], '*') <= 0 for i in Stations[:-1])
    m.addConstrs(t[i]-time_horizon - M * x.sum(i, '*', '*') <= 0 for i in Stations[:-1])

    # Vehicle Loading Constraints
    m.addConstrs(q[(i, v)] <= l_V[(i, v)] for i in Stations[1:-1] for v in Vehicles)
    m.addConstrs(l_V[(start_stations[v], v)] == init_vehicle_load[v] for v in Vehicles)
    m.addConstrs(
        l_V[(j, v)] - vehicle_cap[v] - M * (1-x[(Stations[-1], j, v)]) <= 0 for j in Stations for v in Vehicles)
    m.addConstrs(
        l_V[(j, v)] - vehicle_cap[v] + M * (1 - x[(Stations[-1], j, v)]) >= 0 for j in Stations for v in Vehicles)
    m.addConstrs(l_V[(j, v)] - l_V[(i, v)] - q[(i, v)] - M * (
            1 - x[(i, j, v)]) <= 0 for i in Stations for j in Stations for v in Vehicles)
    m.addConstrs(l_V[(j, v)] - l_V[(i, v)] - q[(i, v)] + M * (
            1 - x[(i, j, v)]) >= 0 for i in Stations for j in Stations for v in Vehicles)

    # Station Loading Constraints
    m.addConstrs(l_F[i]-init_flat_station_load[i] - incoming_flat_rate[i] * t[i] == 0 for i in Stations[1:-1])
    m.addConstrs(l_B[i] - init_station_load[i] - (
            incoming_rate[i] - demand[i])*t[i] - v_S[i] == 0 for i in Stations[1:-1])
    m.addConstrs(q.sum(i, '*') <= l_F[i] for i in Stations[1:-1])
    m.addConstrs(q[(j, v)]-vehicle_cap[v] * x.sum('*', j, '*') <= 0 for j in Stations[1:-1] for v in Vehicles)

    # ------- VIOLATION CONSTRAINTS ------------------------------------------------------------------
    # Add constraints from violations and deviations here

    # ------- OBJECTIVE ------------------------------------------------------------------------------
    m.setObjective(x.sum('*', '*', '*'), GRB.MAXIMIZE)
    m.optimize()
    route_dict = {}
    for v in m.getVars():
        if v.varName[0] == 'x' and v.x == 1:
            t = float(m.getVarByName("t[{}]".format(v.varName[2])).x)
            dist = driving_times[int(v.varName[2])][int(v.varName[4])]
            arch = [int(v.varName[2]), int(v.varName[4]), t, dist]
            if int(v.varName[-2]) not in route_dict.keys():
                route_dict[int(v.varName[-2])] = [arch]
            else:
                route = route_dict[int(v.varName[-2])]
                for i in range(len(route)):
                    if route[i][-1] > t:
                        route.insert(i, arch)
                        break
                    else:
                        if i == len(route_dict[int(v.varName[-2])])-1:
                            route.append(arch)
    draw_routes(route_dict, Stations)
    print(route_dict)
    print("Obj: ", m.objVal)

except GurobiError:
    print("Error")
