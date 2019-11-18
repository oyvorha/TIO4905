import requests
import os

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
