import requests
import os
import json
import pandas as pd

base = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
key = os.environ['KEY']


def get_driving_time(origin_lat, origin_lon, dest_lat, dest_lon):
    parameters = {'origins': "{},{}".format(origin_lon, origin_lat), 'destinations': "{},{}".format(dest_lon, dest_lat),
                  'key': key}
    r = requests.get(base, params=parameters)
    data = r.json()
    origin_address = data['origin_addresses'][0].split(',')[0]
    destination_address = data['destination_addresses'][0].split(',')[0]
    return round(int(data['rows'][0]['elements'][0]['duration']['value']) / 60, 2), origin_address, destination_address


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
    df = pd.DataFrame(columns=['Station ID', 'Station name', 'Station Address', 'latitude', 'longitude'])

    with open("station.json", 'r') as f:
        stations = json.load(f)

    for id, station in stations.items():
        longitude = float(station[0])
        latitude = float(station[1])
        address = get_address(latitude, longitude)
        row = {'Station ID': id, 'Station name': address[0], 'Station Address': address[1], 'latitude': latitude,
               'longitude': longitude}
        df = df.append(row, ignore_index=True)
    df.to_excel("../Output/stations.xlsx", sheet_name="Stations")


if __name__ == "__main__":
    write_all_addresses()
