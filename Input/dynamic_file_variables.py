
class DynamicFileVariables:

    def __init__(self):
        self.start_stations = [3, 4]
        self.init_vehicle_load = [5, 6]
        self.init_station_load = [0, 1, 8, 3, 2, 0]
        self.init_flat_station_load = [0, 6, 2, 6, 7, 0]
        self.ideal_state = [0, 5, 5, 5, 5, 0]
        self.driving_to_start = [3.45, 2.77]
        self.demand = [0, 0.96, 0.58, 0.74, 0.96, 0]
        self.incoming_rate = [0, 0.02, 0.15, 0.15, 0.21, 0]
        self.incoming_flat_rate = [0, 0.6, 0.17, 0.29, 0.15, 0]
