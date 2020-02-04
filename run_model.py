import json
from Input.instance_generator import Instance
from Input.station import Station
from Model.gurobi_model import run_model
from Output.save_output import save_output
from visualize import visualize
from Input.fixed_file_variables import FixedFileVariables
from Input.dynamic_file_variables import DynamicFileVariables


class Subproblem():

    def __init__(self, station_id_list, demand, init_bikes, init_veh, start_st,
                 time_to_start):
        self.fixed = FixedFileVariables()
        self.dynamic = DynamicFileVariables()

        self.station_id_list = station_id_list
        self.dynamic.demand = demand
        self.dynamic.init_station_load = init_bikes
        self.dynamic.init_vehicle_load = init_veh
        self.dynamic.start_stations = start_st
        self.dynamic.time_to_start = time_to_start

        self.n_instance = 10
        self.vehicle_cap = 30
        self.station_cap = 20
        self.flat_rate = 0.3
        self.ideal_state = 10

        self.fixed.time_horizon = 25
        self.fixed.demand_scenario = 'A'
        self.fixed.w_violation = 0.8
        self.fixed.w_dev_obj = 0.1
        self.fixed.w_reward = 0.1
        self.fixed.w_dev_reward = 0.8
        self.fixed.w_driving_time = 0.2

        self.show_image = True
        self.save_output = False

        self.depot = Station(59.93791, 10.73048, None, None, None, None, None, None, None, 465)

    def get_n_stations(self):
        with open("Data_processing/station.json", 'r') as f:
            stations = json.load(f)

        station_objects = []
        counter = 1
        for id, station in stations.items():
            if counter > self.n_instance:
                break
            latitude = float(station[0])
            longitude = float(station[1])
            init_battery_load = station[2][self.fixed.demand_scenario][0]
            init_flat_load = station[2][self.fixed.demand_scenario][1]
            incoming_battery_rate = station[2][self.fixed.demand_scenario][2]
            incoming_flat_rate = station[2][self.fixed.demand_scenario][3]
            outgoing_rate = station[2][self.fixed.demand_scenario][4]
            demand = station[2][self.fixed.demand_scenario][5]
            ideal_state = self.ideal_state
            if self.check_demand(incoming_battery_rate, init_battery_load, demand, ideal_state):
                obj = Station(latitude, longitude, init_battery_load, init_flat_load
                              , incoming_battery_rate, incoming_flat_rate, outgoing_rate,
                              demand, ideal_state, id)
                station_objects.append(obj)
                counter += 1
        return station_objects

    def get_n_stations_sim(self):
        st_objects = list()
        with open("Data_processing/station.json", 'r') as f:
            st_json = json.load(f)

        ind = 0
        for id in self.station_id_list:
            station = st_json[id]
            latitude = float(station[0])
            longitude = float(station[1])
            init_battery_load = self.dynamic.init_station_load[ind]*(1-self.flat_rate)
            init_flat_load = self.dynamic.init_flat_station_load[ind]*self.flat_rate
            incoming_battery_rate = station[2][self.fixed.demand_scenario][2]
            incoming_flat_rate = station[2][self.fixed.demand_scenario][3]
            outgoing_rate = station[2][self.fixed.demand_scenario][4]
            demand = station[2][self.fixed.demand_scenario][5]
            ideal_state = self.ideal_state
            if self.check_demand(incoming_battery_rate, init_battery_load, demand, ideal_state):
                obj = Station(latitude, longitude, init_battery_load, init_flat_load
                              , incoming_battery_rate, incoming_flat_rate, outgoing_rate,
                              demand, ideal_state, id)
                st_objects.append(obj)
            ind += 1
        return st_objects

    def check_demand(self, incoming_bat_rate, init_bat_load, dem, ideal):
        if init_bat_load + self.fixed.time_horizon * (incoming_bat_rate - dem) >= ideal:
            return False
        return True

    def run_model(self):
        if self.station_id_list:
            station_obj = self.get_n_stations_sim()
        else:
            station_obj = self.get_n_stations()
        station_obj.insert(0, self.depot)
        generated_instance = Instance(station_obj, self.fixed, self.dynamic, self.station_cap, self.vehicle_cap,
                                      self.ideal_state)

        model, time = run_model(generated_instance)
        visualize(model, generated_instance.fixed, image=self.show_image)

        if self.save_output:
            save_output(model, time, generated_instance.fixed, generated_instance.dynamic, station_obj)

        return model
