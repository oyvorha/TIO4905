import requests

base = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial"
key = "AIzaSyDT87e1XqA9v2iMsHPKzqELhmP5kRXbVTs"


def get_driving_time(origin_lat, origin_lon, dest_lat, dest_lon):
    parameters = {'origins': "{},{}".format(origin_lat, origin_lon), 'destinations': "{},{}".format(dest_lat, dest_lon),
                  'key': key}
    r = requests.get(base, params=parameters)
    data = r.json()
    return round(int(data['rows'][0]['elements'][0]['duration']['value']) / 60, 2)


print(get_driving_time(63.432251821057207, 10.406996458768845, 63.432503742934855, 10.400386825203896))
