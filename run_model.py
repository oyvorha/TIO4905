import json
from Input.instance_generator import Instance
from Input.station import Station
from Model.gurobi_model import run_model
from Output.save_output import save_output

with open("Data_processing/station.json", 'r') as f:
    stations = json.load(f)

models = []
fixed = []
dynamic = []

instance_runs = [[7, 'A'], [10, 'A'], [15, 'A'], [5, 'B'], [10, 'B'], [15, 'B']]
show_image = True

depot = Station(59.9139, 10.7522, None, None, None, None, None, None, None)


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


for i in range(len(instance_runs)):

    # INPUT VALUES
    n_instance = instance_runs[i][0]
    scenario = instance_runs[i][1]
    time_horizon = 10
    n_vehicles = 2
    ideal_state = 5
    vehicle_cap = 10
    station_cap = 30

    station_obj = get_n_stations(n_instance)
    station_obj.insert(0, depot)
    generated_instance = Instance(len(station_obj)+1, n_vehicles, time_horizon, station_obj, scenario=scenario,
                                  initial_size=n_instance, vehicle_cap=vehicle_cap, station_cap=station_cap)

    model, time = run_model(generated_instance)
    models.append([model, time])
    fixed.append(generated_instance.fixed)
    dynamic.append(generated_instance.dynamic)

save_output(models, fixed, dynamic)
