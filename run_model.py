import json
from Input.instance_generator import Instance
from Input.station import Station
from Model.gurobi_model import run_model
from Output.save_output import save_output
from visualize import visualize

with open("Data_processing/station.json", 'r') as f:
    stations = json.load(f)


def get_n_stations(n):
    station_objects = []
    counter = 1
    for id, station in stations.items():
        if counter > n:
            break
        latitude = float(station[0])
        longitude = float(station[1])
        init_battery_load = station[2][scenario][0]
        init_flat_load = station[2][scenario][1]
        incoming_battery_rate = station[2][scenario][2]
        incoming_flat_rate = station[2][scenario][3]
        outgoing_rate = station[2][scenario][4]
        demand = station[2][scenario][5]
        if check_demand(incoming_battery_rate, init_battery_load, demand, ideal_state):
            obj = Station(latitude, longitude, init_battery_load, init_flat_load
                          , incoming_battery_rate, incoming_flat_rate, outgoing_rate,
                          demand, ideal_state, id)
            station_objects.append(obj)
            counter += 1
    return station_objects


def check_demand(incoming_bat_rate, init_bat_load, dem, ideal):
    if init_bat_load + time_horizon * (incoming_bat_rate - dem) >= ideal:
        return False
    return True


# ------- INPUT VALUES ----------
n_instance = 10
scenario = 'A'
n_vehicles = 1
time_horizon = 25
vehicle_cap = 30
station_cap = 20
ideal_state = station_cap // 2

w_violation = 0.8
w_dev_obj = 0.1
w_reward = 0.1
w_dev_reward = 0.8
w_driving_time = 0.2
show_image = True

depot = Station(59.93791, 10.73048, None, None, None, None, None, None, None, 465)

station_obj = get_n_stations(n_instance)
station_obj.insert(0, depot)
generated_instance = Instance(len(station_obj)+1, n_vehicles, time_horizon, station_obj, scenario=scenario,
                              initial_size=n_instance, vehicle_cap=vehicle_cap, station_cap=station_cap,
                              ideal_state=ideal_state, w_violation=w_violation, w_dev_obj=w_dev_obj,
                              w_reward=w_reward, w_dev_reward=w_dev_reward, w_driving_time=w_driving_time)

model, time = run_model(generated_instance)
visualize(model, generated_instance.fixed, image=show_image)

save_output(model, time, generated_instance.fixed, generated_instance.dynamic, station_obj)
