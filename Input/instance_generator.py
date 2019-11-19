from Input.fixed_file_variables import FixedFileVariables
from Input.dynamic_file_variables import DynamicFileVariables
import numpy as np
from Data_processing.Google_API import get_driving_time_from_id
from Input.generate_Ms import GenMs


class Instance:

    def __init__(self, n_stations, n_vehicles, n_time_hor, stations, scenario='A', initial_size=20, station_cap=30,
                 vehicle_cap=10, ideal_state=5, w_violation=0.8, w_dev_obj=0.1, w_reward=0.1, w_dev_reward=0.8,
                 w_driving_time=0.2):
        self.n_stations = n_stations
        self.n_vehicles = n_vehicles

        self.fixed = FixedFileVariables()
        self.fixed.time_horizon = n_time_hor
        self.fixed.demand_scenario = scenario
        self.fixed.initial_size = initial_size
        self.fixed.w_violation = w_violation
        self.fixed.w_dev_obj = w_dev_obj
        self.fixed.w_reward = w_reward
        self.fixed.w_dev_reward = w_dev_reward
        self.fixed.w_driving_time = w_driving_time

        self.dynamic = DynamicFileVariables()

        self.set_stations()
        self.set_vehicles()
        self.set_station_cap(station_cap)
        self.set_vehicle_cap(vehicle_cap)
        self.set_ideal_state(ideal_state)

        self.set_station_rates(stations)
        self.set_time_matrix(stations)

        self.set_init_vehicle_load(vehicle_cap//2)
        self.set_start_stations()
        self.set_time_to_start()

        self.gen_ms = GenMs(self.fixed, self.dynamic)
        self.write_to_file()

    def set_time_matrix(self, station_obj):
        matrix = np.zeros((self.n_stations, self.n_stations))
        for i in range(self.n_stations-1):
            for j in range(i, self.n_stations-1):
                if i == j:
                    continue
                else:
                    google_response = get_driving_time_from_id(station_obj[i].id, station_obj[j].id)
                    time_x = round(google_response[0], 1)
                    matrix[i][j] = time_x
                    matrix[j][i] = time_x
                    station_obj[i].address = google_response[1]
                    station_obj[j].address = google_response[2]
        self.fixed.driving_times = matrix

    def set_time_to_start(self):
        self.dynamic.driving_to_start = [0] * self.n_vehicles

    def set_stations(self):
        self.fixed.stations = [i for i in range(self.n_stations)]

    def set_vehicles(self):
        self.fixed.vehicles = [i for i in range(self.n_vehicles)]

    def set_start_stations(self):
        start = []
        for i in range(self.n_vehicles):
            if self.n_stations > (i-2):
                start.append(i+1)
            else:
                start.append(0)
        self.dynamic.start_stations = start

    def set_vehicle_cap(self, cap):
        self.fixed.vehicle_cap = [0] * self.n_vehicles
        for i in range(self.n_vehicles):
            self.fixed.vehicle_cap[i] = cap

    def set_init_vehicle_load(self, load):
        self.dynamic.init_vehicle_load = [load for i in self.fixed.vehicles]

    def set_station_cap(self, cap):
        self.fixed.station_cap = [0] * self.n_stations
        for i in self.fixed.stations[1:-1]:
            self.fixed.station_cap[i] = cap

    def set_station_rates(self, station_obj):
        self.dynamic.demand = [0] * self.n_stations
        self.dynamic.incoming_rate = [0] * self.n_stations
        self.dynamic.incoming_flat_rate = [0] * self.n_stations
        self.dynamic.init_flat_station_load = [0] * self.n_stations
        self.dynamic.init_station_load = [0] * self.n_stations
        for station in self.fixed.stations[1:-1]:
            self.dynamic.demand[station] = station_obj[station].demand
            self.dynamic.incoming_rate[station] = station_obj[station].battery_rate
            self.dynamic.incoming_flat_rate[station] = station_obj[station].flat_rate
            self.dynamic.init_station_load[station] = station_obj[station].init_station_load
            self.dynamic.init_flat_station_load[station] = station_obj[station].init_flat_station_load

    def set_ideal_state(self, ideal):
        self.dynamic.ideal_state = [0] * self.n_stations
        for station in self.fixed.stations[1:-1]:
            self.dynamic.ideal_state[station] = ideal

    def write_to_file(self):
        f = open("Input/input_params.txt", 'w')
        f.write("------------ FIXED ------------------------ \n")
        f.write("self.stations = " + str(self.fixed.stations) + "\n")
        f.write("self.vehicles = " + str(self.fixed.vehicles) + "\n")
        f.write("self.time_horizon = " + str(self.fixed.time_horizon) + "\n")
        f.write("self.vehicle_cap = " + str(self.fixed.vehicle_cap) + "\n")
        f.write("self.station_cap = " + str(self.fixed.station_cap) + "\n")
        f.write("self.driving_times = " + repr(self.fixed.driving_times) + "\n")
        f.write("self.parking_time = " + str(self.fixed.parking_time) + "\n")
        f.write("self.handling_time = " + str(self.fixed.handling_time) + "\n")
        f.write("self.M_1 = " + str(self.fixed.M_1) + "\n")
        f.write("self.M_2 = " + str(self.fixed.M_2) + "\n")
        f.write("self.M_3 = " + str(self.fixed.M_3) + "\n")
        f.write("self.M_4 = " + str(self.fixed.M_4) + "\n")
        f.write("self.M_5 = " + str(self.fixed.M_5) + "\n")
        f.write("self.M_6 = " + str(self.fixed.M_6) + "\n")
        f.write("self.M_7A = " + str(self.fixed.M_7A) + "\n")
        f.write("self.M_7B = " + str(self.fixed.M_7B) + "\n")
        f.write("self.M_8A = " + str(self.fixed.M_8A) + "\n")
        f.write("self.M_8B = " + str(self.fixed.M_8B) + "\n")
        f.write("self.M_9 = " + str(self.fixed.M_9) + "\n")
        f.write("self.M_10 = " + str(self.fixed.M_10) + "\n")
        f.write("self.M_11 = " + str(self.fixed.M_11) + "\n")
        f.write("self.M_12 = " + str(self.fixed.M_12) + "\n")
        f.write("self.M_13 = " + str(self.fixed.M_13) + "\n")
        f.write("self.M_14 = " + str(self.fixed.M_14) + "\n")
        f.write("Reward weight deviation = " + str(self.fixed.w_dev_reward) + "\n")
        f.write("Reward weight driving time = " + str(self.fixed.w_driving_time) + "\n")
        f.write("Weight deviation = " + str(self.fixed.w_dev_obj) + "\n")
        f.write("Weight violation = " + str(self.fixed.w_violation) + "\n")
        f.write("Weight reward = " + str(self.fixed.w_reward) + "\n \n")

        f.write("------------ DYNAMIC ------------------------ \n")
        f.write("self.start_stations = " + str(self.dynamic.start_stations) + "\n")
        f.write("self.init_vehicle_load = " + str(self.dynamic.init_vehicle_load) + "\n")
        f.write("self.init_station_load = " + str(self.dynamic.init_station_load) + "\n")
        f.write("self.init_flat_station_load = " + str(self.dynamic.init_flat_station_load) + "\n")
        f.write("self.ideal_state = " + str(self.dynamic.ideal_state) + "\n")
        f.write("self.driving_to_start = " + str(self.dynamic.driving_to_start) + "\n")
        f.write("self.demand = " + str(self.dynamic.demand) + "\n")
        f.write("self.incoming_rate = " + str(self.dynamic.incoming_rate) + "\n")
        f.write("self.incoming_flat_rate = " + str(self.dynamic.incoming_flat_rate) + "\n")
