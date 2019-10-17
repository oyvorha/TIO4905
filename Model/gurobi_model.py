from gurobipy import *
from fixed_file_variables import *
from dynamic_file_variables import *

f = FixedFileVariables()
d = DynamicFileVariables()

try:
    m = Model("Bicycle")

    # ------ SETS -------------
    Stations = f.stations
    Vehicles = f.vehicles

    # ------ FIXED PARAMETERS -------
    time_horizon = f.time_horizon
    vehicle_cap = f.vehicle_cap
    station_cap = f.station_cap
    driving_times = f.driving_times
    parking_time = f.parking_time
    handling_time = f.handling_time
    M = f.M

    # ------- DYNAMIC PARAMETERS ------
    start_stations = d.start_stations
    init_vehicle_load = d.init_vehicle_load
    init_station_load = d.init_station_load
    init_flat_station_load = d.init_flat_station_load
    ideal_state = d.ideal_state
    driving_to_start = d.driving_to_start
    demand = d.demand
    incoming_rate = d.incoming_rate
    incoming_flat_rate = d.incoming_flat_rate

    # ------ VARIABLES --------
    x = m.addVars({(i, j, v) for i in Stations
                     for j in Stations for v in Vehicles}, vtype=GRB.BINARY, name="x")
    t = m.addVars({i for i in Stations}, vtype=GRB.CONTINUOUS, name="t")
    q = m.addVars({(i, v) for i in Stations for v in Vehicles}, vtype=GRB.INTEGER, name="q")
    l_B = m.addVars({(i, v) for i in Stations for v in Vehicles},
                   vtype=GRB.INTEGER, name="l_B")
    l_F = m.addVars({i for i in Stations}, vtype=GRB.INTEGER, name="l_F")
    l_V = m.addVars({(i, v) for i in Stations for v in Vehicles}, vtype=GRB.INTEGER, name="l_V")
    s_I = m.addVars({i for i in Stations}, vtype=GRB.INTEGER, name="s_I")
    s_V = m.addVars({v for v in Vehicles}, vtype=GRB.INTEGER, name="s_V")
    v = m.addVars({i for i in Stations}, vtype=GRB.INTEGER, name="v")
    d = m.addVars({i for i in Stations}, vtype=GRB.CONTINUOUS, name="d")

    # ------- CONSTRAINTS --------
    # Routing constraints
    m.addConstrs(x.sum(start_stations[v], '*', v) == 1 for v in Vehicles)
    m.addConstrs(x.sum('*', Stations[-1], v) == 1 for v in Vehicles)
    for j in Stations[:-1]:
        for v in Vehicles:
            if j != start_stations[v]:
                m.addConstr(x.sum('*', j, v) - x.sum(j, '*', v) == 0)
    m.addConstrs(x.sum('*', j, '*') <= 1 for j in Stations[1:-1])
    m.addConstrs(x.sum('*', 0, v) <= 1 for v in Vehicles)

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

    # ------- OBJECTIVE ----------
    m.setObjective(x.sum('*', '*', '*'), GRB.MAXIMIZE)
    m.optimize()
    for v in m.getVars():
        print(v.varName, v.x)
    print("Obj: ", m.objVal)

except GurobiError:
    print("Error")
