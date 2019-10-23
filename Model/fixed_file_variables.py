
class FixedFileVariables:

    def __init__(self):
        self.stations = [0, 1, 2, 3, 4]
        self.vehicles = [0, 1]
        self.time_horizon = 10
        self.vehicle_cap = [10, 10]
        self.station_cap = 10
        self.driving_times = [[0.0, 3.0, 9.0, 4.0, 6.2], [3.0, 0.0, 2.0, 3.1, 4.7], [9.0, 2.0, 0.0,	2.1, 3.7],
                              [4.0, 3.1, 2.1, 0.0, 2.8], [6.2, 4.7, 3.7, 2.8, 0.0]]
        self.parking_time = 1
        self.handling_time = 1
        self.M = 100
