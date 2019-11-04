
class FixedFileVariables:

    def __init__(self):
        self.stations = [0, 1, 2, 3, 4, 5]
        self.vehicles = [0, 1]
        self.time_horizon = 10
        self.vehicle_cap = [10, 10]
        self.station_cap = [0, 10, 10, 10, 0]
        self.driving_times = [[0, 3.0, 9.0, 4.0, 0], [3.0, 0, 2.0, 3.1, 0], [9.0, 2.0, 0, 2.1, 0],
                              [4.0, 3.1, 2.1, 0, 0], [0, 0, 0, 0, 0]]
        self.parking_time = 1
        self.handling_time = 1
        self.M = 10000
        self.I_B = 5
        self.I_V = 5
        self.w_dev_reward = 0.4
        self.w_driving_time = 0.6
        self.w_violation = 0.5
        self.w_dev_obj = 0.2
        self.w_reward = 0.3
