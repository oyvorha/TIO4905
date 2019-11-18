
class Station:

    def __init__(self, longitude, latitude, bat_load, flat_load, incoming_bat_rate, flat_rate,
                 outgoing, demand, ideal_state):
        self.longitude = longitude
        self.latitude = latitude
        self.init_station_load = bat_load
        self.init_flat_station_load = flat_load
        self.battery_rate = incoming_bat_rate
        self.flat_rate = flat_rate
        self.outgoing_rate = outgoing
        self.demand = demand
        self.ideal_state = ideal_state
        self.address = None
