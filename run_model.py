import json
from Input.instance_generator import Instance
from Input.station import Station


with open("Data_processing/station.json", 'r') as f:
    stations = json.load(f)

# INPUT VALUES
n_stations = 8
scenario = 'B'
time_horizon = 10
n_vehicles = 2


def get_n_stations(n):
    station_objects = []
    for station in stations.items():
        obj = Station(float(station[1][0]), float(station[1][1]), station[1][2][scenario][0], station[1][2][scenario][1], station[1][2][scenario][2],
                      station[1][2][scenario][3], station[1][2][scenario][4], station[1][2][scenario][5])
        station_objects.append(obj)
    return station_objects


station_obj = get_n_stations(n_stations)
Instance(n_stations, n_vehicles, time_horizon, station_obj)
