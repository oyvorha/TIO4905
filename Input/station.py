
class Station():

    def __init__(self, longitude, latitude, bat_load, flat_load, ideal, demand, incoming_rate, flat_rate):
        self.longitude = longitude
        self.latitude = latitude
        self.init_station_load = bat_load
        self.init_flat_station_load = flat_load
        self.ideal_state = ideal
        self.demand = demand
        self.incoming_rate = incoming_rate
        self.incoming_flat_rate = flat_rate