import requests
import os
import json
import pandas as pd

base = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
key = os.environ['KEY']

driving_times = {}


def write_driving_times():
    with open("station.json", 'r') as f:
        station_json = json.load(f)

    for id_1, station_1 in station_json.items():
        longitude_1 = float(station_1[0])
        latitude_1 = float(station_1[1])
        for id_2, station_2 in station_json.items():
            driving_key = str(id_1) + '_' + str(id_2)
            longitude_2 = float(station_2[0])
            latitude_2 = float(station_2[1])
            driving_times[driving_key] = get_driving_time(latitude_1, longitude_1, latitude_2, longitude_2)
        print(driving_times)
    with open('times.json', 'w') as fp:
        json.dump(driving_times, fp)


def get_driving_time(origin_lat, origin_lon, dest_lat, dest_lon):
    parameters = {'origins': "{},{}".format(origin_lon, origin_lat), 'destinations': "{},{}".format(dest_lon, dest_lat),
                  'key': key}
    r = requests.get(base, params=parameters)
    data = r.json()
    origin_address = data['origin_addresses'][0].split(',')[0]
    destination_address = data['destination_addresses'][0].split(',')[0]
    return [round(int(data['rows'][0]['elements'][0]['duration']['value']) / 60, 2), origin_address,
            destination_address]


def get_address(origin_lat, origin_lon):
    dest_lat, dest_lon = 10.7522, 59.9139
    parameters = {'origins': "{},{}".format(origin_lon, origin_lat), 'destinations': "{},{}".format(dest_lon, dest_lat),
                  'key': key}
    r = requests.get(base, params=parameters)
    data = r.json()
    origin_address = data['origin_addresses'][0].split(',')[0]
    full_address = data['origin_addresses'][0].split(',')
    return origin_address, full_address


def write_all_addresses():
    df = pd.DataFrame(columns=['Station ID', 'Station name', 'Station Address', 'latitude', 'longitude', 'init_B_bikes',
                               'init_F_bikes', 'Scenario', 'Demand', 'Ideal State', 'B-bike-rate', 'F-bike-rate'])

    with open("station.json", 'r') as f:
        stations = json.load(f)

    scenarios = ['A', 'B', 'C', 'D', 'E']

    for id, station in stations.items():
        longitude = float(station[0])
        latitude = float(station[1])
        address = get_address(latitude, longitude)
        for scenario in scenarios:
            init_battery_load = station[2][scenario][0]
            init_flat_load = station[2][scenario][1]
            incoming_battery_rate = station[2][scenario][2]
            incoming_flat_rate = station[2][scenario][3]
            demand = station[2][scenario][5]
            row = {'Station ID': id, 'Station name': address[0], 'Station Address': address[1], 'latitude': latitude,
                   'longitude': longitude, 'init_B_bikes': init_battery_load, 'init_F_bikes': init_flat_load,
                   'Scenario': scenario, 'Demand': demand, 'Ideal State': 0, 'B-bike-rate': incoming_battery_rate,
                   'F-bike-rate': incoming_flat_rate}
            df = df.append(row, ignore_index=True)
    df.to_excel("../Output/stations.xlsx", sheet_name="Stations")


def get_driving_time_from_id(station_id_1, station_id_2):
    id_key = str(station_id_1) + '_' + station_id_2
    with open("Data_processing/times.json", 'r') as f:
        time_json = json.load(f)
    return time_json[id_key]
