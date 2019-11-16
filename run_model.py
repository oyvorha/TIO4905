import json
from Input.instance_generator import Instance
from Input.station import Station
from Model.gurobi_model import run_model

with open("Data_processing/station.json", 'r') as f:
    stations = json.load(f)

# INPUT VALUES
n_instance = 20
scenario = 'B'
time_horizon = 30
n_vehicles = 2
ideal_state = 5
vehicle_cap = 10
station_cap = 30


def get_n_stations(n):
    station_objects = []
    counter = 0
    for station in stations.items():
        counter += 1
        if counter > n:
            break
        latitude = float(station[1][0])
        longitude = float(station[1][1])
        init_battery_load = station[1][2][scenario][0]
        init_flat_load = station[1][2][scenario][1]
        incoming_battery_rate = station[1][2][scenario][2]
        incoming_flat_rate = station[1][2][scenario][3]
        outgoing_rate = station[1][2][scenario][4]
        demand = station[1][2][scenario][5]
        if check_demand(incoming_battery_rate, init_battery_load, demand, ideal_state):
            obj = Station(latitude, longitude, init_battery_load, init_flat_load
                          , incoming_battery_rate, incoming_flat_rate, outgoing_rate,
                          demand, ideal_state)
            station_objects.append(obj)
    print(len(station_objects))
    return station_objects


def check_demand(incoming_bat_rate, init_bat_load, dem, ideal):
    if init_bat_load + time_horizon * (incoming_bat_rate - dem) >= ideal:
        return False
    return True


station_obj = get_n_stations(n_instance)
generated_instance = Instance(len(station_obj)+2, n_vehicles, time_horizon, station_obj,
                              vehicle_cap=vehicle_cap, station_cap=station_cap)

model = run_model(generated_instance)

# save_output(model, generated_instance.fixed, generated_instance.dynamic)
