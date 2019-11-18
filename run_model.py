import json
from Input.instance_generator import Instance
from Input.station import Station
from Model.gurobi_model import run_model
from Output.save_output import save_output
from visualize import visualize

with open("Data_processing/station.json", 'r') as f:
    stations = json.load(f)

models = []
fixed = []
dynamic = []


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


# Format of one instance: [#Stations, scenario, time horizon, #vehicles, vehicle_cap, station_cap,
# weight violation, weight deviation, weight reward, reward weight dev, reward weight time]
instance_runs = [[7, 'A', 10, 2, 15, 30, 0.8, 0.1, 0.1, 0.8, 0.2], [7, 'A', 10, 2, 20, 30, 0.8, 0.1, 0.1, 0.8, 0.2],
                 [7, 'B', 10, 2, 20, 30, 0.8, 0.1, 0.1, 0.8, 0.2], [10, 'A', 10, 2, 20, 30, 0.8, 0.1, 0.1, 0.8, 0.2]]

for i in range(len(instance_runs)):

    # ------- INPUT VALUES ----------
    n_instance = instance_runs[i][0]
    scenario = instance_runs[i][1]
    time_horizon = instance_runs[i][2]
    n_vehicles = instance_runs[i][3]
    vehicle_cap = instance_runs[i][4]
    station_cap = instance_runs[i][5]
    ideal_state = station_cap // 2
    w_violation = instance_runs[i][6]
    w_dev_obj = instance_runs[i][7]
    w_reward = instance_runs[i][8]
    w_dev_reward = instance_runs[i][9]
    w_driving_time = instance_runs[i][10]
    show_image = True

    depot = Station(59.9139, 10.7522, None, None, None, None, None, None, None)

    station_obj = get_n_stations(n_instance)
    station_obj.insert(0, depot)
    generated_instance = Instance(len(station_obj)+1, n_vehicles, time_horizon, station_obj, scenario=scenario,
                                  initial_size=n_instance, vehicle_cap=vehicle_cap, station_cap=station_cap,
                                  ideal_state=ideal_state, w_violation=w_violation, w_dev_obj=w_dev_obj,
                                  w_reward=w_reward, w_dev_reward=w_dev_reward, w_driving_time=w_driving_time)

    model, time = run_model(generated_instance)
    models.append([model, time])
    fixed.append(generated_instance.fixed)
    dynamic.append(generated_instance.dynamic)
    station_objs.append(station_obj)
    visualize(model, generated_instance.fixed, image=show_image)

save_output(models, fixed, dynamic, station_objs)
