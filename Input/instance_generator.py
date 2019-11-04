from Model.fixed_file_variables import FixedFileVariables
from Model.dynamic_file_variables import DynamicFileVariables
import numpy as np
import random


class Instance:

    def __init__(self, n_stations, n_vehicles, n_time_hor):
        self.n_stations = n_stations
        self.n_vehicles = n_vehicles
        self.time_horizon = n_time_hor

        self.fixed = FixedFileVariables()
        self.fixed.time_horizon = self.time_horizon

        self.dynamic = DynamicFileVariables()
        self.set_stations()
        self.set_vehicles()
        self.set_time_matrix()
        self.set_station_cap(10)
        self.set_vehicle_cap(10)
        self.set_init_station_load()
        self.set_init_vehicle_load()
        self.set_start_stations()
        self.set_station_rates()
        self.set_ideal_state(5)
        self.set_time_to_start()
        self.write_to_file()

    def set_time_matrix(self):
        time_cap = 15
        matrix = np.zeros((self.n_stations, self.n_stations))
        for i in range(self.n_stations-1):
            for j in range(i, self.n_stations-1):
                if i == j:
                    continue
                else:
                    time_x = round(random.random() * time_cap, 2)
                    matrix[i][j] = time_x
                    matrix[j][i] = time_x
        self.fixed.driving_times = matrix

    def set_time_to_start(self):
        self.dynamic.driving_to_start = [0] * self.n_vehicles
        time_cap = 4
        for vehicle in self.fixed.vehicles:
            self.dynamic.driving_to_start[vehicle] = round(random.random() * time_cap, 2)

    def set_stations(self):
        self.fixed.stations = [i for i in range(self.n_stations)]

    def set_vehicles(self):
        self.fixed.vehicles = [i for i in range(self.n_vehicles)]

    def set_start_stations(self):
        start = []
        for i in range(self.n_vehicles):
            station = random.randint(0, self.n_stations - 2)
            while station in start:
                station = random.randint(0, self.n_stations - 2)
            start.append(station)
        self.dynamic.start_stations = start

    def set_vehicle_cap(self, cap):
        self.fixed.vehicle_cap = [0] * self.n_vehicles
        for i in range(self.n_vehicles):
            self.fixed.vehicle_cap[i] = cap

    def set_init_vehicle_load(self):
        self.dynamic.init_vehicle_load = [random.randint(0, self.fixed.vehicle_cap[i]) for i in self.fixed.vehicles]

    def set_init_station_load(self):
        self.dynamic.init_flat_station_load = [0] * self.n_stations
        self.dynamic.init_station_load = [0] * self.n_stations
        for station in self.fixed.stations[1:-1]:
            battery = random.randint(0, self.fixed.station_cap[station])
            flat = random.randint(0, self.fixed.station_cap[station])
            while battery + flat > self.fixed.station_cap[station]:
                battery = random.randint(0, self.fixed.station_cap[station])
                flat = random.randint(0, self.fixed.station_cap[station])
            self.dynamic.init_station_load[station] = battery
            self.dynamic.init_flat_station_load[station] = flat

    def set_station_cap(self, cap):
        self.fixed.station_cap = [0] * self.n_stations
        for i in self.fixed.stations[1:-1]:
            self.fixed.station_cap[i] = cap

    def set_station_rates(self):
        self.dynamic.demand = [0] * self.n_stations
        self.dynamic.incoming_rate = [0] * self.n_stations
        self.dynamic.incoming_flat_rate = [0] * self.n_stations
        for station in self.fixed.stations[1:-1]:
            demand = round(random.random(), 2)
            battery_rate = round(random.random(), 2)
            flat_rate = round(random.random(), 2)
            while demand < (battery_rate + flat_rate):
                demand = round(random.random(), 2)
                battery_rate = round(random.random(), 2)
                flat_rate = round(random.random(), 2)
            self.dynamic.demand[station] = demand
            self.dynamic.incoming_rate[station] = battery_rate
            self.dynamic.incoming_flat_rate[station] = flat_rate

    def set_ideal_state(self, ideal):
        self.dynamic.ideal_state = [0] * self.n_stations
        for station in self.fixed.stations[1:-1]:
            self.dynamic.ideal_state[station] = ideal

    def write_to_file(self):
        f = open("../Input/input_params.txt", 'w')
        f.write("------------ FIXED ------------------------ \n")
        f.write("Stations = " + str(self.fixed.stations) + "\n")
        f.write("Vehicles = " + str(self.fixed.vehicles) + "\n")
        f.write("Vehicle cap = " + str(self.fixed.vehicle_cap) + "\n")
        f.write("Time horizon = " + str(self.fixed.time_horizon) + "\n")
        f.write("Station capacities = " + str(self.fixed.station_cap) + "\n")
        f.write("Driving times = " + str(self.fixed.driving_times) + "\n")
        f.write("Parking time = " + str(self.fixed.parking_time) + "\n")
        f.write("Handling time = " + str(self.fixed.handling_time) + "\n")
        f.write("Big M = " + str(self.fixed.M) + "\n")
        f.write("Reward weight deviation = " + str(self.fixed.w_dev_reward) + "\n")
        f.write("Reward weight driving time = " + str(self.fixed.w_driving_time) + "\n")
        f.write("Weight deviation = " + str(self.fixed.w_dev_obj) + "\n")
        f.write("Weight violation = " + str(self.fixed.w_violation) + "\n")
        f.write("Weight reward = " + str(self.fixed.w_reward) + "\n \n")

        f.write("------------ DYNAMIC ------------------------ \n")
        f.write("Start stations = " + str(self.dynamic.start_stations) + "\n")
        f.write("Initial vehicle load = " + str(self.dynamic.init_vehicle_load) + "\n")
        f.write("Initial station load = " + str(self.dynamic.init_station_load) + "\n")
        f.write("Initial flat station load = " + str(self.dynamic.init_flat_station_load) + "\n")
        f.write("Ideal state = " + str(self.dynamic.ideal_state) + "\n")
        f.write("Driving time to start = " + str(self.dynamic.driving_to_start) + "\n")
        f.write("Demand = " + str(self.dynamic.demand) + "\n")
        f.write("Incoming battery bike rate = " + str(self.dynamic.incoming_rate) + "\n")
        f.write("Incoming flat bike rate = " + str(self.dynamic.incoming_flat_rate) + "\n")
