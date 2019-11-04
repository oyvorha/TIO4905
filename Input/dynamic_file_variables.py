
class DynamicFileVariables:

    def __init__(self):
        self.start_stations = [2, 4]
        self.init_vehicle_load = [2, 8]
        self.init_station_load = [0, 3, 5, 5, 3, 0] # [0, 0, 1, 3, 0, 0]
        self.init_flat_station_load = [0, 0, 3, 2, 0, 0]
        self.ideal_state = [0, 5, 5, 5, 0, 0]
        self.driving_to_start = [2, 1]
        self.demand = [0, 1, 5, 8, 0, 0]
        self.incoming_rate = [0, 0.5, 0.2, 0.5, 0, 0]
        self.incoming_flat_rate = [0, 1, 0.8, 0.4, 0, 0]
