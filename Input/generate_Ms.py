import numpy as np


class GenMs:

    def __init__(self, fixed, dynamic):
        self.fixed = fixed
        self.dynamic = dynamic
        self.set_all_Ms()

    def get_max_t(self):
        max_t = []
        for station in self.fixed.stations:
            time_horizon = self.fixed.time_horizon
            handling_time = self.fixed.handling_time
            max_Qv = max(self.fixed.vehicle_cap)
            max_Qs = max(self.fixed.station_cap)
            max_qB = min(max_Qv, max_Qs)
            park_time = self.fixed.parking_time
            max_dist = np.amax(self.fixed.driving_times, axis=0)[station]
            max_t_st = time_horizon + handling_time*max_qB + park_time + max_dist
            max_t.append(max_t_st)
        return max_t

    def getM_1(self):
        M_1 = []
        max_t_array = self.get_max_t()
        park_time = self.fixed.parking_time
        handling_time = self.fixed.handling_time
        for i in range (len(self.fixed.stations)):
            i_list = []
            max_t_i = max_t_array[i]
            max_qv = max(self.fixed.vehicle_cap)
            max_qs = self.fixed.station_cap[i]
            max_qb = min(max_qv, max_qs)
            for j in range(len(self.fixed.stations)):
                max_t_j = 0
                d_time = self.fixed.driving_times[i][j]
                j_val = max_t_i + park_time + handling_time*max_qb + d_time - max_t_j
                i_list.append(j_val)
            M_1.append(i_list)
        return M_1


    def getM_2(self):
        M_2 = max(self.get_max_t()) - self.fixed.time_horizon
        return M_2

    def getM_3(self):
        M_3 = self.get_max_t()
        return M_3

    def getM_4(self):
        M_4 = max(self.fixed.vehicle_cap)
        return M_4

    def getM_5(self):
        max_qv = max(self.fixed.vehicle_cap)
        max_qs = max(self.fixed.station_cap)
        res = min(max_qv, max_qs)
        M_5 = 2*res
        return M_5

    def getM_6(self):
        M_6 = self.get_max_t()
        return M_6

    def getM_7(self):
        M_7 = self.fixed.station_cap
        return M_7

    def getM_8(self):
        M_8 = self.fixed.station_cap
        return M_8

    def getM_9(self):
        station_cap = self.fixed.station_cap
        flow_batt = self.dynamic.incoming_rate
        demand = self.dynamic.demand
        net_d = np.array(flow_batt) - np.array(demand)
        time = np.array(self.get_max_t()) - self.fixed.time_horizon
        M_9 = -(np.array(station_cap) + net_d*time) #PS jeg er litt usikker på fortegn her
        return M_9

    def getM_10(self):
        station_cap = self.fixed.station_cap
        flow_flat = self.dynamic.incoming_flat_rate
        time = np.array(self.get_max_t()) - self.fixed.time_horizon
        M_10 = np.array(station_cap) + flow_flat*time
        return M_10

    def getM_11(self):
        M_11 = np.absolute(self.dynamic.demand) * self.fixed.time_horizon
        return M_11

    def getM_12(self):
        M_12 = np.absolute(self.dynamic.demand) * (np.array(self.get_max_t())-self.fixed.time_horizon)
        return M_12

    def getM_13(self):
        M_13 = np.absolute(self.dynamic.demand) * (np.array(self.get_max_t()) - self.fixed.time_horizon)
        return M_13

    def getM_14(self):
        max_tv = []
        for vehicle in self.fixed.vehicles:
            handling_time = self.fixed.handling_time
            max_Qv = self.fixed.vehicle_cap[vehicle]
            max_Qs = max(self.fixed.station_cap)
            max_qB = min(max_Qv, max_Qs)
            park_time = self.fixed.parking_time
            max_dist = np.amax(self.fixed.driving_times)
            tv = park_time + handling_time * max_qB + max_dist
            max_tv.append(tv - 0 + self.fixed.time_horizon)
        return max_tv

    def set_all_Ms(self):
        self.fixed.M_1 = self.getM_1()
        self.fixed.M_2 = self.getM_2()
        self.fixed.M_3 = self.getM_3()
        self.fixed.M_4 = self.getM_4()
        self.fixed.M_5 = self.getM_5()
        self.fixed.M_6 = self.getM_6()
        self.fixed.M_7 = self.getM_7()
        self.fixed.M_8 = self.getM_8()
        self.fixed.M_9 = self.getM_9()
        self.fixed.M_10 = self.getM_10()
        self.fixed.M_11 = self.getM_11()
        self.fixed.M_12 = self.getM_12()
        self.fixed.M_13 = self.getM_13()
        self.fixed.M_14 = self.getM_14()
